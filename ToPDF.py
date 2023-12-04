import datetime
import os
import sqlite3
import subprocess
import jinja2
from plyer import notification


conn = sqlite3.connect('data/bm.db')
def notification_msg(title,msg):
    notification.notify(
        title=title,
        message=msg,
        app_name="Business Manager",  # Replace with your app's name
        app_icon = "data/ico.ico",
        timeout=10  # Specify how long the notification should stay visible (in seconds)
    )

def GetChromeLocation():
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome_path):
        return chrome_path
    else:
        if os.path.exists('data/browser.cfg'):
            with open('data/browser.cfg','r') as f:
                location = f.readline().replace("\n","")
                if os.path.exists(location):
                    return location
                else:
                    notification_msg('Chrome Location Incorrect', 'Please setup browser location in \n"data/browser.cfg"')
                    return False
        else:
            with open('data/browser.cfg','w') as f:
                f.write('')
            notification_msg('Chrome Not Found', 'Please setup browser location in \n"data/browser.cfg"')
            return False


class ToPDF:
    def __init__(self, invoice):
        self.invoice = invoice
        conn = sqlite3.connect('data/bm.db')
        cursor = conn.cursor()
        cursor = conn.execute(f"SELECT * from invoice WHERE id='{invoice}'")
        for row in cursor:
            customerid = row[1]
            date = row[2]
        cursor = conn.execute(f"SELECT * FROM customer WHERE id='{customerid}'")  # id,name,address,tel,email

        for row in cursor:
            c = []
            for item in row[2:]:
                if item == "":
                    continue
                else:
                    c.append(item)

            data = '<br>'.join(str(elem) for elem in c)
            name = row[1]
            address = row[2]
            tel = row[3]
            email = row[4]
        cursor = conn.execute(
            f"SELECT id,jobid,service,price FROM service WHERE invoice='{invoice}' ORDER BY jobid ASC")  # id,invoice,invoicenum,jobid,service,price
        services = []
        for row in cursor:
            services.append({"jobid": row[1], "service": row[2], "price": int(row[3])})

        num = 0
        total = 0
        rows = ''
        for row in services:
            num = num + 1
            dnum = '{:02d}'.format(num)
            sample = f"<tr><td>{dnum}</td><td>{'{:04d}'.format(row['jobid'])}</td><td>{row['service']}</td><td class='ipri'>Rs.{row['price']}.00</td></tr>"
            total = total + row['price']
            rows = rows + sample
        if (len(services) < 10):
            for row in range(0, 12 - len(services)):
                sample = f"<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class='ipri'>&nbsp;</td></tr>"
                rows = rows + sample

        context = {'name': name, 'invoice': '{:05d}'.format(invoice),
                   'date': datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y %b %d'), 'data': data,
                   'rows': rows, 'total': total}

        template_loader = jinja2.FileSystemLoader('./')
        template_env = jinja2.Environment(loader=template_loader)

        template = template_env.get_template("data/templates/invoice.html")
        output_text = template.render(context)

        file = open('data/outputs/invoice.html', 'w')
        file.write(output_text)
        file.close()

        path = os.path.abspath('data/outputs/invoice.html')

        chrome_path = GetChromeLocation()

        if chrome_path:
            html_file_path = path  # Replace with the actual file path of your HTML file
            absolute_path = os.path.join(os.getcwd(), html_file_path)
            html_file_url = "file://" + absolute_path

            command = [
                chrome_path,
                "--incognito",
                "--app=" + html_file_url
            ]

            subprocess.Popen(command)




class GenerateReceipt:

    def __init__(self, receipt_id):
        def customerDetailsToSingleString(address, tel, email):
            details = [address, tel, email]
            details = [s for s in details if s]
            details = "<br>".join(details)
            return (details)


        conn = sqlite3.connect('data/bm.db')
        cursor = conn.cursor()
        error = False
        try:
            date,invoice_id,method_id,amount = conn.execute(f"SELECT date,invoice,method,amount from payment WHERE id='{receipt_id}'").fetchone()
            method = conn.execute(f"SELECT method from payment_method WHERE id='{method_id}'").fetchone()[0]
            customer_id = conn.execute(f"SELECT customerid from invoice WHERE id='{invoice_id}'").fetchone()[0]
            name,address,tel,email = conn.execute(f"SELECT name,address,tel,email FROM customer WHERE id={customer_id}").fetchone()
            total = conn.execute(f"SELECT SUM(price) FROM service WHERE invoice={invoice_id}").fetchone()[0]
            paid = conn.execute(f"SELECT SUM(amount) FROM payment WHERE invoice={invoice_id} and id<={receipt_id}").fetchone()[0]
            unpaid = int(total) - int(paid)
        except:
            error = True

        if not(error):
            customer_details = customerDetailsToSingleString(address,tel,email)
            receipt_id = "{:06}".format(receipt_id)
            invoice_id = "{:04}".format(invoice_id)
            context = {
                'receipt_id' :receipt_id,
                'name':name,
                'customer_details':customer_details,
                'invoice_id':invoice_id,
                'date':date,
                'method':method,
                'amount':amount,
                'unpaid':unpaid
            }
            template_loader = jinja2.FileSystemLoader('./')
            template_env = jinja2.Environment(loader=template_loader)

            template = template_env.get_template("data/templates/receipt.html")
            output_text = template.render(context)

            file = open('data/outputs/receipt.html', 'w')
            file.write(output_text)
            file.close()

            path = os.path.abspath('data/outputs/receipt.html')

            chrome_path = GetChromeLocation()

            if chrome_path:
                html_file_path = path  # Replace with the actual file path of your HTML file
                absolute_path = os.path.join(os.getcwd(), html_file_path)
                html_file_url = "file://" + absolute_path

                command = [
                    chrome_path,
                    "--incognito",
                    "--app=" + html_file_url
                ]

                subprocess.Popen(command)


class GeneratePaymentSummary:

    def __init__(self, invoice_id):
        def customerDetailsToSingleString(address, tel, email):
            details = [address, tel, email]
            details = [s for s in details if s]
            details = "<br>".join(details)
            return (details)


        conn = sqlite3.connect('data/bm.db')
        cursor = conn.cursor()
        error = False
        try:
            total = conn.execute(f"SELECT COALESCE(SUM(price),0) from service WHERE invoice='{invoice_id}'").fetchone()[0]
            customer_id = conn.execute(f"SELECT customerid from invoice WHERE id={invoice_id}").fetchone()[0]
            name,address,tel,email = conn.execute(f"SELECT name,address,tel,email from customer WHERE id={customer_id}").fetchone()
            paid = conn.execute(f"SELECT COALESCE(SUM(amount),0) FROM payment WHERE invoice={invoice_id}").fetchone()[0]
            unpaid = int(total)-int(paid)

            payment_methods = conn.execute(f"SELECT id,method FROM payment_method").fetchall()
            method ={}
            for instance in payment_methods:
                method[instance[0]]=instance[1]
            payments =[]
            payment_list = conn.execute(f"SELECT id,date,method,amount FROM payment WHERE invoice={invoice_id}").fetchall()
            for instance in payment_list:
                payments.append((instance[0],instance[1],method[instance[2]],instance[3]))

            tabledata = ""
            for row in payments:
                tabledata = tabledata + f'''
                                    <tr>
                        <td>{"{:06}".format(row[0])}</td>
                        <td>{row[1]}</td>
                        <td>{row[2]}</td>
                        <td class='ipri'>Rs.{row[3]}.00</td>
                    </tr>
                '''
            if len(payments)==0:
                tabledata = tabledata + f'''
                                                    <tr>
                                        <td>&numsp;</td>
                                        <td>&numsp;</td>
                                        <td>&numsp;</td>
                                        <td class='ipri'>&numsp;</td>
                                    </tr>
                                '''

            payment_info = '''            
            <div class="paymentinfo">
                <div class="paymenttitle">
                    Payment Info
                </div>
                <div class="details">
                    <table>
                        <tr>
                            <td class="infotitle">Account No</td>
                            <td class="data">00000000</td>
                        </tr>
                        <tr>
                            <td class="infotitle">Name</td>
                            <td class="data">Harindu Bandara</td>
                        </tr>
                        <tr>
                            <td class="infotitle">Bank</td>
                            <td class="data">ABC Bank (Colombo)</td>
                        </tr>
                    </table>
                </div>

            </div>'''

            if unpaid == 0:
                payment_info = "<br><br><br><br>"
                ok = f'''<tr>
    
                            <td class="tsub" colspan = 2>Full Payment Success</td>
                        </tr>'''
            else:
                ok = f'''<tr>
                            <td class="ttitle">Remaining Amount:&nbsp;</td>
                            <td class="tsub">Rs.{unpaid}.00</td>
                        </tr> '''
            invoice_id = "{:04}".format(int(invoice_id))

            context = {
                'name':name,
                'customer_details':customerDetailsToSingleString(address,tel,email),
                'invoice_id':"{:04}".format(invoice_id),
                'invoice_total':total,
                'paid':paid,
                'unpaid':unpaid,
                'table':tabledata,
                'payment_info':payment_info,
                'ok':ok
            }

            template_loader = jinja2.FileSystemLoader('./')
            template_env = jinja2.Environment(loader=template_loader)

            template = template_env.get_template("data/templates/payment_summary.html")
            output_text = template.render(context)

            file = open('data/outputs/payment_summary.html', 'w')
            file.write(output_text)
            file.close()

            path = os.path.abspath('data/outputs/payment_summary.html')

            chrome_path = GetChromeLocation()

            if chrome_path:
                html_file_path = path  # Replace with the actual file path of your HTML file
                absolute_path = os.path.join(os.getcwd(), html_file_path)
                html_file_url = "file://" + absolute_path

                command = [
                    chrome_path,
                    "--incognito",
                    "--app=" + html_file_url
                ]

                subprocess.Popen(command)

        except:
            error = True