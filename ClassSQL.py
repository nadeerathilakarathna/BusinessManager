import sqlite3

from ToPDF import conn


class BusinessSQL:
    def __init__(self,db_name = 'data/bm.db'):
        self.conn = sqlite3.connect(db_name)

    def DeleteInvoice(self,id):
        conn.execute(f"DELETE FROM payment WHERE invoice = '{id}'")
        conn.commit()
        conn.execute(f"DELETE FROM service WHERE invoice = '{id}'")
        conn.commit()
        conn.execute(f"DELETE FROM invoice WHERE id = '{id}'")
        conn.commit()
        return True

    def GetMaxInvoiceID(self):
        return conn.execute(f"SELECT MAX(id) from invoice").fetchone()[0]

    def GetMaxPaymentID(self):
        return conn.execute(f"SELECT MAX(id) from payment").fetchone()[0]

    def GetMaxJobID(self):
        return conn.execute(f"SELECT MAX(jobid) from service").fetchone()[0]

    def SelectAll(self, table, order='id'):
        result = []
        query = f"SELECT * FROM {table} ORDER BY {order} ASC"
        cursor = conn.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def AddCustomer(self, name, address, tel, email):
        if conn.execute(f"SELECT COUNT(*) FROM customer WHERE name='{name}'").fetchone()[0]:
            return False
        else:
            conn.execute(f"INSERT INTO customer (name, address,tel,email) VALUES ('{name}','{address}' ,'{tel}','{email}')")
            conn.commit()
            return True


    def GetCustomer(self,id):
        result = []
        cursor = conn.execute(f"SELECT * FROM customer WHERE id={id}")
        for row in cursor:
            result.append(row)
        return result[0]

    def UpdateCustomer(self, id,name,address='',tel='',email=''):
        conn.execute("UPDATE customer SET name=?, address=?, tel=?, email=? WHERE id=?", (name, address,tel,email,id))
        conn.commit()

    def AddService(self,id,invoice, jobid, service, price):
        conn.execute(
            f"INSERT INTO service(invoice,jobid,service,price) VALUES ('{invoice}','{jobid}' ,'{service}','{price}')")
        conn.commit()
        return True

    def AddInvoice(self,invoiceid, customerid, date, folder):
        conn.execute(f"INSERT INTO invoice(id,customerid,date,folder) VALUES ('{invoiceid}','{customerid}','{date}','{folder}')")
        conn.commit()


    def AddPayment(self,date,invoice,method,reference,description,amount):
        def run(sql):
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchone()[0]
        #cursor = conn.cursor()
        total = (run(f'''SELECT COALESCE(SUM(price),0) FROM service WHERE invoice={invoice}'''))
        paid = (run(f'''SELECT COALESCE(SUM(amount),0) FROM payment WHERE invoice={invoice}'''))
        topay = total-paid
        if int(topay)>= int(amount):
            currentid = conn.execute(f"SELECT COALESCE(MAX(id),0) from payment").fetchone()[0]+1
            conn.execute(f"INSERT INTO payment(id,date,invoice,method,reference,description,amount) VALUES ('{currentid}','{date}','{invoice}','{method}','{reference}','{description}','{amount}')")
            conn.commit()
            return True
        else:
            return False


    def AddPaymentMethod(self,name):
        if not (len(conn.execute(f"SELECT * FROM payment_method WHERE method='{name}'").fetchall())):
            conn.execute(f"INSERT INTO payment_method (method) VALUES('{name}')")
            conn.commit()
            return True
        else:
            return False

    def SelectAllCustomersInThisName(self,name):
        return conn.execute(f"SELECT * FROM customer Where Name='{name}'")

    def getInvoiceFolder(self,invoiceid):
        return conn.execute(f"SELECT folder FROM invoice Where id='{invoiceid}'").fetchone()[0]

    def CheckAlreadyHasInvoice(self,invoiceid):
        service = conn.execute(f"SELECT COUNT(*) FROM service WHERE invoice='{int(invoiceid)}'").fetchone()[0]
        invoice_id = conn.execute(f"SELECT COUNT(*) FROM invoice WHERE id='{int(invoiceid)}'").fetchone()[0]
        if (invoice_id !=0 or service !=0):
            return True
        else:
            return False

    def CheckAlreadyHasCustomer(self, customername):
        return len(conn.execute(f"SELECT * FROM customer WHERE name='{customername}' LIMIT 1").fetchall())

    def AllCustomersGivenName(self,name):
        return conn.execute(f"SELECT * FROM customer WHERE name='{name}' LIMIT 1").fetchall()

    def FindInvoice(self,keyword):

        cursor = conn.cursor()
            # Use the SQL query to search for the keyword in the customer name or email
        query = f"""
            SELECT invoice.id, customer.name, invoice.date, SUM(service.price) AS total
            FROM customer
            INNER JOIN invoice ON customer.id = invoice.customerid
            INNER JOIN service ON invoice.id = service.invoice
            WHERE customer.name LIKE ? OR invoice.id LIKE ? OR invoice.date LIKE ?
            GROUP BY invoice.id, customer.name, invoice.date
            ORDER BY invoice.id DESC
        """

        # Execute the query with the keyword as a parameter
        cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))

        # Fetch all the results from the query
        results = cursor.fetchall()

        # Print the results
        res = []
        for row in results:
            invoice_id, customer_name, invoice_date, total = row
            res.append([invoice_id,customer_name,invoice_date,total])

#            print(f"Invoice ID: {invoice_id}, Customer Name: {customer_name}, Date: {invoice_date}, Total: {total}")
        return res

    def FindInvoiceByCondition(self,condition,keyword):
        conditions= ["    All    ", "    Paid    ", "Remaining"]

        cursor = conn.cursor()
        # Use the SQL query to search for the keyword in the customer name or email
        query = f"""
                SELECT invoice.id, customer.name, invoice.date, SUM(service.price) AS total_services,
                (SELECT COALESCE(SUM(amount),0) FROM payment WHERE payment.invoice = invoice.id) AS total_payments 
                FROM customer
                INNER JOIN invoice ON customer.id = invoice.customerid
                INNER JOIN service ON invoice.id = service.invoice
                WHERE customer.name LIKE ? OR invoice.id LIKE ? OR invoice.date LIKE ?
                GROUP BY invoice.id, customer.name, invoice.date
                ORDER BY invoice.id DESC;"""

        # Execute the query with the keyword as a parameter
        cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))

        # Fetch all the results from the query
        results = cursor.fetchall()

        # Print the results
        res = []
        for row in results:

            invoice_id, customer_name, invoice_date, total,paid = row
            unpaid = int(total)-int(paid)
            if (condition == conditions[0]):
                if (unpaid==0):
                    unpaid='SUCCESS'
                res.append([invoice_id, customer_name, invoice_date, total,unpaid])
            elif (condition == conditions[1]):
                if (unpaid!=0):
                    continue
                if (unpaid==0):
                    unpaid='SUCCESS'
                res.append([invoice_id, customer_name, invoice_date, total,unpaid])
            elif (condition == conditions[2]):
                if (unpaid==0):
                    continue
                res.append([invoice_id, customer_name, invoice_date, total, unpaid])
        #            print(f"Invoice ID: {invoice_id}, Customer Name: {customer_name}, Date: {invoice_date}, Total: {total}")
        return res

    def GetInvoiceDetails(self,invoiceid):
        if invoiceid:
            cursor = conn.cursor()
            sql = f'''SELECT id,customerid,date,folder FROM invoice WHERE id='{invoiceid}';
            '''
            invoice_data = cursor.execute(sql).fetchone()
            if(bool(invoice_data)):
                sql = f'''SELECT name,address,tel,email FROM customer WHERE id={invoice_data[1]};
                '''
                customer_data = cursor.execute(sql).fetchone()

                if(bool(customer_data)):
                    sql = f'''SELECT id,jobid,service,price FROM service WHERE invoice={invoiceid} ORDER BY jobid ASC;
                '''
                    service_data = cursor.execute(sql).fetchall()
                    if (bool(service_data)):
                        sql = f'''SELECT COALESCE(SUM(price),0) as total FROM service WHERE invoice={invoiceid};'''
                        total = cursor.execute(sql).fetchone()[0]
                        sql = f'''SELECT COALESCE(SUM(amount),0) as paid FROM payment WHERE invoice={invoiceid};'''
                        paid = cursor.execute(sql).fetchone()[0]
                        unpaid = int(total) - int(paid)
                        if unpaid == 0:
                            unpaid = "PAYMENT SUCCESS"
                        else:
                            unpaid = f"Outstanding Balance : {unpaid}"
                        res = {'invoice':invoice_data,'customer':customer_data,'service':service_data,'total':total,'unpaid':unpaid}
                        return res
                    else:
                        total = 0
                        sql = f'''SELECT COALESCE(SUM(amount),0) as paid FROM payment WHERE invoice={invoiceid};'''
                        paid = cursor.execute(sql).fetchone()[0]
                        unpaid = int(total) - int(paid)
                        if unpaid == 0:
                            unpaid = "PAYMENT SUCCESS"
                        else:
                            unpaid = f"Outstanding Balance : {unpaid}"
                        res = {'invoice':invoice_data,'customer':customer_data,'service':service_data,'total':total,'unpaid':unpaid}
                        return res
        return False

    def UpdateInvoiceDate(self,invoiceid,date):
        sql =  f'''UPDATE invoice SET date='{date}' WHERE id={invoiceid};'''
        conn.execute(sql)
        conn.commit()
        return True

    def UpdateInvoiceFolder(self,invoiceid,folder):
        sql = f'''UPDATE invoice SET folder='{folder}' WHERE id={invoiceid};'''
        conn.execute(sql)
        conn.commit()
        return True

    def UpdateService(self,id,jobid,service,price):
        if jobid.isdigit() and service != "" and price.isdigit():
            sql = f"UPDATE service SET jobid = '{jobid}', service = '{service}', price = {price} WHERE id = {id};"
            conn.execute(sql)
            conn.commit()
            return True

    def DeleteService(self,id):
        sql = f"DELETE FROM service WHERE id = {id};"
        conn.execute(sql)
        conn.commit()
        return True

    def GetPayments(self,s=''):
        cursor = conn.cursor()
        sql = f'''
                SELECT
                    payment.id,
                    payment.date,
                    payment.invoice,
                    payment_method.method AS method,
                    payment.reference,
                    payment.description,
                    payment.amount
                FROM
                    payment
                INNER JOIN
                    payment_method ON payment.method = payment_method.id
                WHERE
                    payment.invoice LIKE '%{s}%'
                    OR payment_method.method LIKE '%{s}%'
                    OR payment.id LIKE '%{s}%'
                    OR payment.date LIKE '%{s}%'
                    OR payment.reference LIKE '%{s}%'
                    OR payment.description LIKE '%{s}%'
                    OR payment.amount LIKE '%{s}%'
                ORDER BY payment.id DESC;
                
                '''
        try:
            invoice_data = cursor.execute(sql).fetchall()
            return invoice_data
        except:
            return False

    def UpdatePayment(self,id,date,reference,description,amount):
        amount =int(amount.split('.')[0])
        if str(amount).isdigit():
            sql = f"UPDATE payment SET date = '{date}', reference = '{reference}', description = '{description}', amount = '{int(amount)}' WHERE id = {id};"
            conn.execute(sql)
            conn.commit()
            return True
        else:
            return False

    def GetPaymentsByInvoice(self,invoiceid):
        cursor = conn.cursor()
        sql = f'''
                SELECT
                    payment.id,
                    payment.date,
                    payment.invoice,
                    payment_method.method AS method,
                    payment.reference,
                    payment.description,
                    payment.amount
                FROM
                    payment
                INNER JOIN
                    payment_method ON payment.method = payment_method.id
                WHERE
                    payment.invoice ={invoiceid};
                '''
        try:
            invoice_data = cursor.execute(sql).fetchall()
            return invoice_data
        except:
            return False


    def GetDetailsRelatedPayment(self,invoiceid):
        cursor = conn.cursor()
        sql = f'''SELECT customerid,date FROM invoice WHERE id={invoiceid};'''
        try:
            cursor_data = cursor.execute(sql).fetchone()
            customer_id = cursor_data[0]
            invoice_date = cursor_data[1]
            sql = f'''SELECT COALESCE(SUM(price),0),COALESCE(COUNT(service),0) FROM service WHERE invoice={invoiceid};'''
            try:
                total = cursor.execute(sql).fetchone()[0]
                items = cursor.execute(sql).fetchone()[1]
                sql = f'''SELECT COALESCE(SUM(amount),0) FROM payment WHERE invoice={invoiceid};'''
                try:
                    paid_amount = cursor.execute(sql).fetchone()[0]
                    sql = f'''SELECT name,address,tel,email FROM customer WHERE id={customer_id};'''
                    try:
                        cursor_data =cursor.execute(sql).fetchone()
                        if (cursor_data):
                            res = {
                                'customer':cursor_data[0],'customer_details':f"{cursor_data[1]}\n{cursor_data[2]}\n{cursor_data[3]}",
                                'date':invoice_date,'items':items,'total':total,'paid':paid_amount,'topay':int(total)-int(paid_amount)
                                   }
                            return res
                        else:
                            return False
                    except:
                        return False
                except:
                    return False
            except:
                return False
        except:
            return False

    def DeletePayment(self,paymentid):
        sql = f'''DELETE FROM payment WHERE id={paymentid};'''
        conn.execute(sql)
        conn.commit()
        return True

    def GetPaymentMethods(self):
        cursor = conn.cursor()
        sql = '''SELECT * FROM payment_method;'''
        d = {}
        try:
            paymentmethods = cursor.execute(sql).fetchall()
            for payment in paymentmethods:
                d[payment[1]]=payment[0]
            return d
        except:
            return d



    def A(self,invoiceid):
        cursor = conn.cursor()
        sql = f'''SELECT COALESCE(SUM(price),0),COALESCE(COUNT(service),0) FROM service WHERE invoice={invoiceid};'''
        conn.execute(sql)
        conn.commit()
        return True



# methods = [
#     ('2023-06-02',1,1,'120452369874512F','The Trasnfer of the day',5000),
#     ('2023-05-02',5,3,'120452123874512F','The Next Transfer',2000),
#     ('2023-04-02',7,2,'452352369874512F','Initial Transfer',200),
# ]
# for method in methods:
#     sql = f'''INSERT INTO payment(date, invoice, method, reference, description, amount)
#     VALUES('{method[0]}', '{method[1]}', '{method[2]}', '{method[3]}', '{method[4]}', '{method[5]}');'''
#     conn.execute(sql)
# conn.commit()

#
# db = BusinessSQL()
# print(db.AddPaymentMethod("BOC Accounst"))


#
# [(7, '2023-06-02', 1, 'Cash', '', 'Mony on hand', 1000)]