import os
import threading
import time
import tkinter
from tkinter import filedialog

import customtkinter
from PIL import Image

from ClassSQL import BusinessSQL

db = BusinessSQL()
from ToPDF import ToPDF
from ToPDF import GenerateReceipt
from ToPDF import GeneratePaymentSummary

from datetime import datetime
import datetime


class Home:
    def HomeScreen(self, root):
        def create_AddCustomerScreen():
            destroy_HomeScreen()
            AddCustomer.Screen(root)

        def destroy_HomeScreen():
            frame.forget()

        def create_CreateInvoiceScreen():
            destroy_HomeScreen()
            CreateInvoice.Screen(root)

        def create_ManageCustomerScreen():
            destroy_HomeScreen()
            ManageCustomer.Screen(root)

        def create_InvoicesScreen():
            destroy_HomeScreen()
            Invoices.Screen(root)

        def create_PaymentsScreen():
            destroy_HomeScreen()
            PaymentDetails.Screen(root)

        icon_add_customer = customtkinter.CTkImage(Image.open("data/icons/add_user.png"), size=(20, 20), )
        icon_add_invoice = customtkinter.CTkImage(Image.open("data/icons/add_invoice.png"), size=(20, 20), )
        icon_payment = customtkinter.CTkImage(Image.open("data/icons/payment.png"), size=(20, 20), )
        icon_invoice = customtkinter.CTkImage(Image.open("data/icons/invoice.png"), size=(20, 20), )
        icon_manage_customer = customtkinter.CTkImage(Image.open("data/icons/manage_user.png"), size=(20, 20), )

        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        fhome = customtkinter.CTkFrame(master=frame)
        fhome.pack(pady=100, padx=100, fill="both", expand=True)

        b1 = customtkinter.CTkButton(master=fhome, text="Add Customer", command=create_AddCustomerScreen,)
        b1.pack(padx=10, pady=10, ipadx=25, side="top", expand=True, anchor='s')
        b2 = customtkinter.CTkButton(master=fhome, text="Create Invoice", command=create_CreateInvoiceScreen,)
        b2.pack(padx=10, pady=(5,20), ipadx=25, side="top")

        b3 = customtkinter.CTkButton(master=fhome, text="Invoices", command=create_InvoicesScreen,)
        b3.pack(padx=10, pady=10, ipadx=25, side="top", anchor='n')
        b5 = customtkinter.CTkButton(master=fhome, text="Payments", command=create_PaymentsScreen,)
        b5.pack(padx=10, pady=(5,20), ipadx=25, side="top", anchor='n')


        b4 = customtkinter.CTkButton(master=fhome, text="Manage Customer", command=create_ManageCustomerScreen,)
        b4.pack(padx=10, pady=10, ipadx=25, side="top", expand=True, anchor='n')



        root.title("Business Manager")  # set the window title
        root.iconbitmap("data/icon.ico")  # set the window icon


class AddCustomer:
    def Screen(root):

        def backToHomeScreen():
            facus.forget()
            gui = Home()
            gui.HomeScreen(root=root)

        def CheckCustomer():
            if len(ace2.get()) == 0:
                ace2.configure(border_color='red')
                ace2.mainloop()
                ace2.configure(border_color='black')
                ace2.mainloop()

            name = ace2.get().title()
            address = ace3.get().title()
            tel = ace4.get()
            email = ace5.get().lower()

            if (db.AddCustomer(name, address, tel, email)):
                ace2.delete(0, customtkinter.END)
                ace3.delete(0, customtkinter.END)
                ace4.delete(0, customtkinter.END)
                ace5.delete(0, customtkinter.END)
                ace2.focus()

                def abcd():
                    alertlabel.configure(text=f"Added : {name}")
                    alertlabel.update()
                    time.sleep(3)
                    alertlabel.configure(text="")
                    alertlabel.update()

                thread = threading.Thread(target=abcd)
                thread.start()

            else:
                def abcd():
                    alertlabel.configure(text=f"A name has already been registered as a match", text_color="Red")
                    alertlabel.update()
                    time.sleep(3)
                    alertlabel.configure(text="", text_color="gray70")
                    alertlabel.update()

                thread = threading.Thread(target=abcd)
                thread.start()

        facus = customtkinter.CTkFrame(master=root)
        facus.pack(pady=100, padx=100, fill="both", expand=True)

        acl1 = customtkinter.CTkLabel(master=facus, text="Add Customer")

        acl2 = customtkinter.CTkLabel(master=facus, text="Name: ", )
        acl3 = customtkinter.CTkLabel(master=facus, text="Address: ", )
        acl4 = customtkinter.CTkLabel(master=facus, text="Mobile: ", )
        acl5 = customtkinter.CTkLabel(master=facus, text="Email: ", )

        ace2 = customtkinter.CTkEntry(master=facus, placeholder_text="Name", width=300)
        ace3 = customtkinter.CTkEntry(master=facus, placeholder_text="Address", width=300)
        ace4 = customtkinter.CTkEntry(master=facus, placeholder_text="Telephone", width=300)
        ace5 = customtkinter.CTkEntry(master=facus, placeholder_text="Email", width=300)

        acl1.grid(row=0, column=0, columnspan=2, pady=10)

        acl2.grid(row=2, column=0, sticky='e', pady=5)
        acl3.grid(row=3, column=0, sticky='e', pady=5)
        acl4.grid(row=4, column=0, sticky='e', pady=5)
        acl5.grid(row=5, column=0, sticky='e', pady=5)

        ace2.grid(row=2, column=1, sticky='w')
        ace3.grid(row=3, column=1, sticky='w')
        ace4.grid(row=4, column=1, sticky='w')
        ace5.grid(row=5, column=1, sticky='w')

        facus.grid_columnconfigure(0, weight=1)
        facus.grid_columnconfigure(1, weight=1)
        facus.grid_rowconfigure(6, weight=0)

        acbtn1 = customtkinter.CTkButton(master=facus, text="Add", command=CheckCustomer)
        acbtn1.grid(row=6, column=0, columnspan=2, pady=15)

        alertlabel = customtkinter.CTkLabel(master=facus, text="", text_color="gray70")
        alertlabel.grid(row=7, column=0, columnspan=2, pady=15)

        button = customtkinter.CTkButton(master=facus, text='⌂', command=backToHomeScreen, width=20, height=20,
                                         corner_radius=80)
        button.configure(fg_color='transparent')
        button.place(x=10, y=10)


class CreateInvoice:

    def Screen(root):

        frame = root
        fci = customtkinter.CTkFrame(master=frame)

        def backToHomeScreen():
            fci.forget()
            gui = Home()
            gui.HomeScreen(root=root)

        def Add_Item_RETURN(*args):
            if cie6.get() == "":
                cie6.focus()
            elif cie7.get() == "":
                cie7.focus()
            elif cie8.get() == "":
                cie8.focus()
            else:
                Add_Item()

        def Process_Invoice():
            project_location = ''
            if (bool(entry_project_location.get())):
                if os.path.exists(entry_project_location.get()) and os.path.isdir(entry_project_location.get()):
                    project_location = entry_project_location.get()

            if not (cie2.get().isdigit()):
                return -1

            elif (db.CheckAlreadyHasInvoice(cie2.get())):
                cie2.focus()
                cie2.select_range(0, customtkinter.END)
                return -1

            elif var.get() == "":
                return -1

            elif db.CheckAlreadyHasCustomer(var.get()) != 1:
                return -1

            elif len(invoice_data) == 0:
                return -1
            else:
                cursor = db.AllCustomersGivenName(var.get())
                if (len(cursor)) == 1:
                    for row in cursor:
                        cid = row[0]
                        db.AddInvoice(int(cie2.get()), cid, cie3.get(), project_location)
                        c = 0
                        for item in invoice_data:
                            c = c + 1
                            db.AddService(int(item[0]), int(cie2.get()), item[0], item[1], item[2])

                        a = int(cie2.get())
                        p = threading.Thread(target=ToPDF, args=(a,))
                        p.start()

                        # PrintInvoice(int(cie2.get()))
                else:
                    return -1

        global t
        t = 0
        invoice_data = []

        def open_file_browser():
            file_path = tkinter.filedialog.askdirectory()
            if file_path:
                entry_project_location.delete(0, customtkinter.END)
                entry_project_location.insert(0, file_path)
            else:
                entry_project_location.delete(0, customtkinter.END)

        def Add_Item():
            global t
            if (cie6.get().isdigit() and cie7.get() != "" and cie8.get().isdigit()):
                invoice_data.append([int(cie6.get()), cie7.get().title(), int(cie8.get())])

                ail1 = customtkinter.CTkLabel(cif1, text="{:02d}".format(t + 1), justify=tkinter.LEFT, )
                ail2 = customtkinter.CTkLabel(cif1, text="{:04d}".format(int(cie6.get())), justify=tkinter.LEFT)
                ail3 = customtkinter.CTkLabel(cif1, text=cie7.get().title(), justify=tkinter.LEFT)
                ail4 = customtkinter.CTkLabel(cif1, text="Rs." + str(cie8.get()), justify=tkinter.LEFT)

                cif1.grid_columnconfigure(2, weight=1)
                cif1.grid_columnconfigure(0, weight=5)
                cif1.grid_columnconfigure(1, weight=5)
                cif1.grid_columnconfigure(3, weight=5)

                ail1.grid(row=t, column=0, padx=10, sticky='w')
                ail2.grid(row=t, column=1, padx=10, sticky='w')
                ail3.grid(row=t, column=2, padx=10, sticky='w')
                ail4.grid(row=t, column=3, padx=10, sticky='e')

                nowcie6 = int(cie6.get()) + 1
                cie6.delete(0, customtkinter.END)
                cie7.delete(0, customtkinter.END)
                cie8.delete(0, customtkinter.END)

                cie6.insert(0, nowcie6)
                t = t + 1

                price = 0
                for item in invoice_data:
                    price = price + item[-1]
                cil12.configure(text=f"Total: Rs.{price}.00")
                cie7.focus()

        lastid = db.GetMaxInvoiceID()
        lastjobid = db.GetMaxJobID()

        try:
            nowid = lastid + 1
            jobid = lastjobid + 1
        except:
            nowid = 1
            jobid = 1

        today = datetime.date.today()
        today = today.strftime("%Y-%m-%d")

        chooselist = []
        allcustomers = db.SelectAll('customer', 'name')

        for row in allcustomers:
            chooselist.append(row[1])

        fci.pack(pady=5, padx=20, fill="both", expand=True, )

        cil1 = customtkinter.CTkLabel(master=fci, text="Create Invoice")
        cil2 = customtkinter.CTkLabel(master=fci, text="Invoice")
        cil3 = customtkinter.CTkLabel(master=fci, text="Date")
        cil4 = customtkinter.CTkLabel(master=fci, text="Customer")
        cil5 = customtkinter.CTkLabel(master=fci, text="", justify=tkinter.LEFT)  # details about customer

        cie2 = customtkinter.CTkEntry(master=fci, placeholder_text="00001", width=200)
        cie3 = customtkinter.CTkEntry(master=fci, placeholder_text="2023-12-21", width=200)

        label_project_location = customtkinter.CTkLabel(master=fci, text="Directory")
        label_project_location.grid(row=3, column=0, padx=5, sticky='w', pady=10)

        entry_project_location = customtkinter.CTkEntry(master=fci, placeholder_text="", width=160)
        entry_project_location.grid(row=3, column=1, sticky='w')

        icon_location = customtkinter.CTkImage(Image.open("data/icons/location.png"), size=(20, 20), )
        button_project_location = customtkinter.CTkButton(master=fci, text="", image=icon_location, width=0,
                                                          command=open_file_browser)
        button_project_location.grid(row=3, column=1, sticky='e')

        def callback2(*args):
            if var.get() != "":
                cursor = db.SelectAllCustomersInThisName(var.get())
                for row in cursor:
                    customerdata = []
                    for data in row[1:]:
                        if data != "":
                            customerdata.append(data)
                    customerdata = '\n'.join(customerdata)
                    cil5.configure(text=customerdata)

        var = tkinter.StringVar()
        cicb4 = customtkinter.CTkComboBox(master=fci, width=200, values=chooselist, variable=var, )
        cicb4.configure(state='readonly')
        var.trace('w', callback2)

        cie6 = customtkinter.CTkEntry(master=fci, placeholder_text="Job ID", )
        cie7 = customtkinter.CTkEntry(master=fci, placeholder_text="Design Description")
        cie8 = customtkinter.CTkEntry(master=fci, placeholder_text="Price")

        cil12 = customtkinter.CTkLabel(master=fci, text="Total: Rs.0.00", justify=tkinter.RIGHT, font=("Arial", 20))
        cil12.configure(text="Total: Rs.0.00")

        cib9 = customtkinter.CTkButton(master=fci, text="Add", command=Add_Item, width=5)
        cib11 = customtkinter.CTkButton(master=fci, text="Create Invoice", command=Process_Invoice)

        cif1 = customtkinter.CTkScrollableFrame(master=fci)

        cie2.insert(0, "{:05d}".format(nowid))
        cie3.insert(0, today)
        cie6.insert(0, jobid)

        cil1.grid(row=0, column=0, columnspan=6, sticky="ew")

        cil2.grid(row=1, column=0, pady=10, sticky="w", padx=5)
        cil3.grid(row=2, column=0, pady=10, sticky="w", padx=5)
        cil4.grid(row=4, column=0, pady=10, padx=5, sticky="w")
        cil5.grid(row=5, column=0, columnspan=2, pady=5, sticky='n')

        cie2.grid(row=1, column=1, )
        cie3.grid(row=2, column=1, )

        cicb4.grid(row=4, column=1)

        cif1.grid(row=1, column=2, rowspan=5, columnspan=4, sticky="nesw", padx=10, pady=10)
        fci.grid_rowconfigure(5, weight=1)
        fci.grid_columnconfigure(3, weight=1, )

        cie6.grid(row=8, column=2, padx=3)
        cie7.grid(row=8, column=3, sticky="ew", padx=3)
        cie8.grid(row=8, column=4, padx=3)

        cil12.grid(row=9, column=4, columnspan=2, pady=10, sticky='e', padx=10)
        cib11.grid(row=10, column=0, columnspan=9, pady=40, sticky="n")

        cib9.grid(row=8, column=5, padx=10)

        root.bind('<Return>', Add_Item_RETURN)

        button = customtkinter.CTkButton(master=fci, text='⌂', width=20, height=20,
                                         corner_radius=80, command=backToHomeScreen)
        button.configure(fg_color='transparent')
        button.place(x=10, y=10)




class ManageCustomer:
    def Screen(root):

        def backToHomeScreen():
            fecus.forget()
            gui = Home()
            gui.HomeScreen(root=root)

        frame = root
        result = (db.SelectAll('customer', "name"))
        chooselist = []
        for row in result:
            chooselist.append(row[1])

        fecus = customtkinter.CTkFrame(master=frame)
        fecus.pack(pady=100, padx=100, fill="both", expand=True)

        acl1 = customtkinter.CTkLabel(master=fecus, text="Edit Customer")

        acl2 = customtkinter.CTkLabel(master=fecus, text="Name: ", )
        acl3 = customtkinter.CTkLabel(master=fecus, text="Address: ", )
        acl4 = customtkinter.CTkLabel(master=fecus, text="Mobile: ", )
        acl5 = customtkinter.CTkLabel(master=fecus, text="Email: ", )

        ace2 = customtkinter.CTkEntry(master=fecus, placeholder_text="Name", width=300)
        ace3 = customtkinter.CTkEntry(master=fecus, placeholder_text="Address", width=300)
        ace4 = customtkinter.CTkEntry(master=fecus, placeholder_text="Telephone", width=300)
        ace5 = customtkinter.CTkEntry(master=fecus, placeholder_text="Email", width=300)

        en = customtkinter.CTkEntry(master=fecus, placeholder_text="Name", width=300)

        def callback(*arg):
            if var.get() != "":
                for i in range(0, len(chooselist)):
                    if var.get() == chooselist[i]:
                        customer = db.GetCustomer(result[i][0])
                        en.delete(0, 'end')
                        en.insert(0, customer[0])
                        ace2.delete(0, 'end')
                        ace2.insert(0, customer[1])
                        ace3.delete(0, 'end')
                        ace3.insert(0, customer[2])
                        ace4.delete(0, 'end')
                        ace4.insert(0, customer[3])
                        ace5.delete(0, 'end')
                        ace5.insert(0, customer[4])

        def CheckCustomer():
            if ace2.get() == "":
                ace2.configure(border_color="red")
            else:
                db.UpdateCustomer(en.get(), ace2.get().title(), ace3.get().title(), ace4.get(), ace5.get().lower())
                en.delete(0, customtkinter.END)
                ace2.delete(0, customtkinter.END)
                ace3.delete(0, customtkinter.END)
                ace4.delete(0, customtkinter.END)
                ace5.delete(0, customtkinter.END)
                accb1.focus()

        var = tkinter.StringVar()
        accb1 = customtkinter.CTkComboBox(master=fecus, values=chooselist, width=300, variable=var, )
        accb1.grid(row=1, column=1, columnspan=1, sticky='w', pady=15)
        accb1.configure(state='readonly')
        var.trace('w', callback)

        acl1.grid(row=0, column=0, columnspan=2, pady=10)

        acl2.grid(row=2, column=0, sticky='e', pady=5)
        acl3.grid(row=3, column=0, sticky='e', pady=5)
        acl4.grid(row=4, column=0, sticky='e', pady=5)
        acl5.grid(row=5, column=0, sticky='e', pady=5)

        ace2.grid(row=2, column=1, sticky='w')
        ace3.grid(row=3, column=1, sticky='w')
        ace4.grid(row=4, column=1, sticky='w')
        ace5.grid(row=5, column=1, sticky='w')

        fecus.grid_columnconfigure(0, weight=1)
        fecus.grid_columnconfigure(1, weight=1)
        fecus.grid_rowconfigure(6, weight=0)

        acbtn1 = customtkinter.CTkButton(master=fecus, text="Update", command=CheckCustomer)
        acbtn1.grid(row=6, column=0, columnspan=2, pady=15)

        button = customtkinter.CTkButton(master=fecus, text='⌂', width=20, height=20,
                                         corner_radius=80, command=backToHomeScreen)
        button.configure(fg_color='transparent')
        button.place(x=10, y=10)


class Invoices:
    def Screen(root):
        icon_delete = customtkinter.CTkImage(Image.open("data/icons/delete.png"), size=(20, 20))
        icon_location = customtkinter.CTkImage(Image.open("data/icons/location.png"), size=(20, 20))
        icon_print = customtkinter.CTkImage(Image.open("data/icons/print.png"), size=(20, 20))
        icon_edit = customtkinter.CTkImage(Image.open("data/icons/edit.png"), size=(20, 20), )

        def findInvoice(event):
            for w in subframe.winfo_children():
                w.destroy()

            invoices = db.FindInvoiceByCondition(category_var.get(),entry.get())

            create_buttons(invoices)
            # subframe.destroy()
            # subframe.update()

        def backToHomeScreen():
            fi.forget()
            gui = Home()
            gui.HomeScreen(root=root)

        def segmentmoved(event):
            findInvoice('')

        frame = root
        fi = customtkinter.CTkFrame(master=frame)
        fi.pack(pady=5, padx=20, fill="both", expand=True, )

        cil1 = customtkinter.CTkLabel(master=fi, text="Invoices", )
        cil1.pack(pady=0, )

        datalist = db.FindInvoiceByCondition("    All    ",'')

        category_var = customtkinter.StringVar(value="    All    ")  # set initial value
        segmented_category = customtkinter.CTkSegmentedButton(master=fi,
                                                              values=["    All    ", "    Paid    ", "Remaining"],
                                                              variable=category_var, dynamic_resizing=False, width=400,
                                                              font=customtkinter.CTkFont(size=13, ),command=segmentmoved
                                                              )
        segmented_category.pack(pady=10)


        entry = customtkinter.CTkEntry(master=fi,
                                       width=250,
                                       height=25, placeholder_text="Search")
        entry.pack(pady=10)
        entry.bind('<KeyRelease>', findInvoice)





        subframe = customtkinter.CTkScrollableFrame(master=fi)
        subframe.configure(height=300, )
        subframe.pack(pady=20, padx=20, fill="both", )

        invoices = db.FindInvoiceByCondition("    All    ","")

        subframe.grid_columnconfigure(0, weight=1)
        subframe.grid_columnconfigure(1, weight=5)
        subframe.grid_columnconfigure(2, weight=5)
        subframe.grid_columnconfigure(3, weight=5)
        subframe.grid_columnconfigure(4, weight=5)
        subframe.grid_columnconfigure(5, weight=2)
        subframe.grid_columnconfigure(6, weight=2)
        subframe.grid_columnconfigure(7, weight=2)
        c = 0

        def printItem(item):
            p = threading.Thread(target=ToPDF, args=(item[0],))
            p.start()

        def deleteItem(invoiceid):
            db.DeleteInvoice(invoiceid[0])
            for w in subframe.winfo_children():
                w.destroy()
            invoices = db.FindInvoice(entry.get())
            create_buttons(invoices)

        def locateItem(invoiceid):
            folder = db.getInvoiceFolder(invoiceid)
            if os.path.exists(folder) and os.path.isdir(folder):
                os.startfile(folder)

            # print(item[0])
            # Function to delete the given item and its corresponding button

        #      buttons[item].grid_forget()  # Remove the button from the grid
        #     del buttons[item]  # Remove the button reference from the dictionary
        #    items.remove(item)  # Remove the item from the list

        def create_buttons(invoices):
            c = 0
            for invoice in invoices:
                bg_button = subframe.cget('fg_color')

                label_invoice = customtkinter.CTkLabel(master=subframe, text=invoice[0])
                label_invoice.grid(row=c, column=0, sticky='w', pady=2, padx=10)

                label_name = customtkinter.CTkLabel(master=subframe, text=invoice[1], anchor='w')
                label_name.grid(row=c, column=1, sticky='w', padx=5)

                label_date = customtkinter.CTkLabel(master=subframe, text=invoice[2])
                label_date.grid(row=c, column=2, sticky='w', padx=5, )

                label_total = customtkinter.CTkLabel(master=subframe, text=invoice[3])
                label_total.grid(row=c, column=3, sticky='e', padx=5)

                label_remaining = customtkinter.CTkLabel(master=subframe, text=invoice[4])
                label_remaining.grid(row=c, column=4, sticky='e', padx=5)

                button_print = customtkinter.CTkButton(master=subframe, text="", image=icon_print, width=20,
                                                       command=lambda i=invoice: printItem(i), fg_color=bg_button)
                button_print.grid(row=c, column=5, sticky='e', padx=5)
                button_prints[invoice[0]] = button_print

                button_loc = customtkinter.CTkButton(master=subframe, text="", image=icon_location, width=20,
                                                     command=lambda i=invoice: locateItem(i[0]), fg_color=bg_button)
                button_loc.grid(row=c, column=6, padx=5, sticky='e')
                button_locs[invoice[0]] = button_loc

                # button_del = customtkinter.CTkButton(master=subframe, image=icon_delete, text="",width=20,fg_color=bg_button,command=lambda i=invoice: deleteItem(i))
                # button_del.grid(row=c, column=6,pady=6, padx=5,sticky = 'e')
                # button_dels[invoice[0]] = button_del

                button_del = customtkinter.CTkButton(master=subframe, image=icon_edit, text="", width=20,
                                                     fg_color=bg_button,
                                                     command=lambda i=invoice: EditInvoice.Screen(frame, i[0]))
                button_del.grid(row=c, column=7, pady=6, padx=5, sticky='e')
                button_dels[invoice[0]] = button_del

                label_name.columnconfigure(0, minsize=100)

                c = c + 1

        #                print(button_prints)

        button_prints = {}
        button_dels = {}
        button_locs = {}

        create_buttons(invoices)
        button = customtkinter.CTkButton(master=fi, text='⌂', width=20, height=20,
                                         corner_radius=80, command=backToHomeScreen)
        button.configure(fg_color='transparent')
        button.place(x=10, y=10)


class EditInvoice:
    def Screen(root, invoiceid):

        def findInvoice(event):

            def editservice(service):
                if list_service[service]['edit'].cget('image') == icon_edit:
                    list_service[service]['title'].configure(state=customtkinter.NORMAL, border_width=1)
                    list_service[service]['price'].configure(state=customtkinter.NORMAL, border_width=1)
                    list_service[service]['jobid'].configure(state=customtkinter.NORMAL, border_width=1)
                    list_service[service]['edit'].configure(image=icon_done)
                else:
                    service_title = list_service[service]['title'].get()
                    service_jobid = list_service[service]['jobid'].get()
                    service_price = list_service[service]['price'].get()
                    if (db.UpdateService(service, service_jobid, service_title, service_price)):
                        list_service[service]['edit'].configure(image=icon_edit)
                        list_service[service]['title'].configure(state=customtkinter.DISABLED, border_width=0)
                        list_service[service]['price'].configure(state=customtkinter.DISABLED, border_width=0)
                        list_service[service]['jobid'].configure(state=customtkinter.DISABLED, border_width=0)
                        findInvoice(root)

            def deleteservice(service):
                print(service)
                if (db.DeleteService(service)):
                    findInvoice(root)

            for w in frame_service.winfo_children():
                w.destroy()

            entry_add_jobid.delete(0, customtkinter.END)
            entry_add_title.delete(0, customtkinter.END)
            entry_add_price.delete(0, customtkinter.END)
            frame_add_service.grid_forget()
            button_add.grid(column=0, row=4, columnspan=7, sticky='es', padx=30, pady=25)

            invoices = db.GetInvoiceDetails(entry_invoice.get())


            if (invoices):
                label_cus_name.configure(text=invoices['customer'][0])
                label_cus_data.configure(
                    text=f'{invoices["customer"][1]}\n{invoices["customer"][2]}\n{invoices["customer"][3]}')
                entry_date.configure(state=customtkinter.NORMAL)
                entry_date.delete(0, customtkinter.END)
                entry_date.insert(0, invoices['invoice'][2])
                entry_date.configure(state=customtkinter.DISABLED)
                entry_folder.configure(state=customtkinter.NORMAL)
                entry_folder.delete(0, customtkinter.END)
                entry_folder.insert(0, invoices['invoice'][3])
                entry_folder.configure(state=customtkinter.DISABLED)
                label_total.configure(text=f"Total: {invoices['total']}.00")
                label_amount_paid.configure(text=invoices['unpaid'])
            else:
                label_cus_name.configure(text="")
                label_cus_data.configure(text="")

                entry_date.configure(state=customtkinter.NORMAL)
                entry_date.delete(0, customtkinter.END)
                entry_date.configure(state=customtkinter.DISABLED)
                button_date.configure(image=icon_edit_small)

                entry_folder.configure(state=customtkinter.NORMAL)
                entry_folder.delete(0, customtkinter.END)
                entry_folder.configure(state=customtkinter.DISABLED)

                label_total.configure(text="")
                label_amount_paid.configure(text="")

            c = 0
            list_service = {}

            if(bool(label_cus_name.cget('text'))):
                button_delete.configure(state=customtkinter.NORMAL)
                button_payment.configure(state=customtkinter.NORMAL)
            else:
                button_delete.configure(state=customtkinter.DISABLED)
                button_payment.configure(state=customtkinter.DISABLED)


            if invoices:
                frame_service.columnconfigure(0, weight=1)
                frame_service.columnconfigure(1, weight=2)
                frame_service.columnconfigure(2, weight=5)
                frame_service.columnconfigure(3, weight=3)
                frame_service.columnconfigure(4, weight=2)
                frame_service.columnconfigure(5, weight=2)

                for service in invoices['service']:
                    entry_service_number = customtkinter.CTkEntry(master=frame_service, border_width=0, width=50)
                    entry_service_number.grid(column=0, row=c, pady=5, sticky='ew', padx=5)
                    entry_service_number.insert(0, c + 1)
                    entry_service_number.configure(state=customtkinter.DISABLED)

                    entry_service_jobid = customtkinter.CTkEntry(master=frame_service, border_width=0, width=50)
                    entry_service_jobid.grid(column=1, row=c, sticky='ew', padx=5)
                    entry_service_jobid.insert(0, f'{service[1]:04d}')
                    entry_service_jobid.configure(state=customtkinter.DISABLED)

                    entry_service_title = customtkinter.CTkEntry(master=frame_service, border_width=0)
                    entry_service_title.grid(column=2, row=c, sticky='ew', padx=5)
                    entry_service_title.insert(0, service[2])
                    entry_service_title.configure(state=customtkinter.DISABLED)

                    entry_service_price = customtkinter.CTkEntry(master=frame_service, border_width=0, width=80)
                    entry_service_price.grid(column=3, row=c, sticky='ew', padx=5)
                    entry_service_price.insert(0, service[3])
                    entry_service_price.configure(state=customtkinter.DISABLED)

                    button_service_edit = customtkinter.CTkButton(master=frame_service, text="", image=icon_edit,
                                                                  fg_color=frame_service.cget('fg_color'), width=0,
                                                                  height=0,
                                                                  command=lambda i=service: editservice(i[0]))
                    button_service_edit.grid(column=4, row=c, sticky='we')

                    button_service_delete = customtkinter.CTkButton(master=frame_service, text="", image=icon_delete,
                                                                    width=0, height=0,
                                                                    fg_color=frame_service.cget('fg_color'),
                                                                    command=lambda i=service: deleteservice(i[0]))
                    button_service_delete.grid(column=5, row=c, sticky='we')

                    list_service[service[0]] = {'id': entry_service_number, 'jobid': entry_service_jobid,
                                                'title': entry_service_title, 'price': entry_service_price,
                                                'edit': button_service_edit, 'delete': button_service_delete}
                    # print(c)
                    c = c + 1

        def truefalse(root, callback):
            def msg_yes():
                frame_msg.destroy()
                callback(True)

            def msg_no():
                frame_msg.destroy()
                callback(False)

            frame_msg = customtkinter.CTkToplevel(root)

            frame_msg.title("Edit Invoice")  # set the window title
            frame_msg.iconbitmap("data/icon.ico")

            width = 400  # Width
            height = 150  # Height

            screen_width = f.winfo_screenwidth()  # Width of the screen
            screen_height = f.winfo_screenheight()  # Height of the screen

            # Calculate Starting X and Y coordinates for Window
            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)

            frame_msg.geometry('%dx%d+%d+%d' % (width, height, x + 125, y - 40))

            label_msg = customtkinter.CTkLabel(master=frame_msg, text="Do you want to delete?")
            button_yes = customtkinter.CTkButton(master=frame_msg, text="Yes", command=msg_yes)
            button_no = customtkinter.CTkButton(master=frame_msg, text="No", command=msg_no)

            label_msg.grid(column=0, row=0, columnspan=2)
            button_yes.grid(column=0, row=1, sticky='ew', padx=20, pady=20)
            button_no.grid(column=1, row=1, sticky='ew', padx=20, pady=20)

            frame_msg.rowconfigure(0, weight=1)
            frame_msg.columnconfigure(0, weight=1)
            frame_msg.columnconfigure(1, weight=1)

            frame_msg.grab_set()
            frame_msg.mainloop()

        def deleteinvoice():
            def continue_delete(confirm):
                if confirm:
                    if entry_invoice.get().isdigit():
                        if db.DeleteInvoice(entry_invoice.get()):
                            f.destroy()

            truefalse(root, continue_delete)

        def pressaddservice():
            if (bool(label_cus_name.cget('text'))):
                frame_add_service.grid(column=0, row=4, columnspan=7, sticky='wes', padx=25, pady=(0, 10))
                button_add_service.configure(image=icon_done)
                button_add.grid_forget()
                entry_add_jobid.delete(0, customtkinter.END)
                entry_add_jobid.insert(0, (db.GetMaxJobID()) + 1)

        def addservice():
            if entry_add_jobid.get().isdigit() and entry_add_title.grid() != "" and entry_add_price.get().isdigit():
                if db.AddService("", entry_invoice.get(), entry_add_jobid.get(), entry_add_title.get(),
                                 entry_add_price.get()):
                    entry_add_jobid.delete(0, customtkinter.END)
                    entry_add_title.delete(0, customtkinter.END)
                    entry_add_price.delete(0, customtkinter.END)
                    frame_add_service.grid_forget()
                    button_add.grid(column=0, row=4, columnspan=7, sticky='es', padx=30, pady=25)
                    findInvoice("")

        def openfolder(self=''):
            if os.path.exists(entry_folder.get()) and os.path.isdir(entry_folder.get()):
                os.startfile(entry_folder.get())

        def setdate():
            if (entry_date.cget('state') == 'disabled'):
                if (bool(label_cus_name.cget('text'))):
                    entry_date.configure(state=customtkinter.NORMAL)
                    button_date.configure(image=icon_done_small)

            else:
                try:
                    if datetime.datetime.strptime(entry_date.get(), '%Y-%m-%d'):
                        if (db.UpdateInvoiceDate(entry_invoice.get(), entry_date.get())):
                            entry_date.configure(state=customtkinter.DISABLED)
                            button_date.configure(image=icon_edit_small)
                except ValueError:
                    print("Wrong")

        def setfolder():
            if (bool(label_cus_name.cget('text'))):
                file_path = filedialog.askdirectory()
                if file_path:
                    if db.UpdateInvoiceFolder(entry_invoice.get(), file_path):
                        entry_folder.configure(state=customtkinter.NORMAL)
                        entry_folder.delete(0, customtkinter.END)
                        entry_folder.insert(0, file_path)
                        entry_folder.configure(state=customtkinter.DISABLED)
                else:
                    if db.UpdateInvoiceFolder(entry_invoice.get(), ''):
                        entry_folder.configure(state=customtkinter.NORMAL)
                        entry_folder.delete(0, customtkinter.END)
                        entry_folder.configure(state=customtkinter.DISABLED)
        def gotopayment():
            f.withdraw()
            gui = Payment.Screen(root,entry_invoice.get())
            #<class 'customtkinter.windows.ctk_tk.CTk'>
            #gui = Payment().Screen(root)
            #gui.Screen(invoiceid=8)

        def on_up_key(event):
            current_value = entry_invoice.get()
            if current_value.isdigit():
                new_value = int(current_value) + 1
                entry_invoice.delete(0, customtkinter.END)
                entry_invoice.insert(0, new_value)

        def on_down_key(event):
            current_value = entry_invoice.get()
            if current_value.isdigit() and int(current_value) > 1:
                new_value = int(current_value) - 1
                entry_invoice.delete(0, customtkinter.END)
                entry_invoice.insert(0, new_value)

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        f = customtkinter.CTkToplevel(root)
        # f.attributes('-topmost', 'true')

        f.title("Edit Invoice")  # set the window title
        f.iconbitmap("data/icon.ico")

        width = 1000  # Width
        height = 650  # Height

        screen_width = f.winfo_screenwidth()  # Width of the screen
        screen_height = f.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        f.geometry('%dx%d+%d+%d' % (width, height, x + 50, y - 40))

        f.columnconfigure(0, weight=1)
        # f.columnconfigure(1, weight=2)
        # f.columnconfigure(2, weight=5)
        # f.columnconfigure(3, weight=2)
        # f.columnconfigure(4, weight=2)
        f.rowconfigure(0, weight=1)

        subframe = customtkinter.CTkFrame(master=f)
        subframe.grid(column=0, row=0, padx=10, pady=10, sticky='nwse')

        subframe.columnconfigure(0, weight=2, minsize=250)
        subframe.columnconfigure(1, weight=2)

        subframe.columnconfigure(2, weight=1)

        subframe.columnconfigure(3, weight=1)
        subframe.columnconfigure(4, weight=1)
        subframe.columnconfigure(5, weight=1)
        subframe.columnconfigure(6, weight=2)

        label_main_title = customtkinter.CTkLabel(master=subframe, text="Edit Invoice")
        label_main_title.grid(column=0, row=0, sticky='we', columnspan=7, pady=10)

        label_invoice = customtkinter.CTkLabel(master=subframe, text="Invoice")
        label_invoice.grid(column=5, row=1, sticky='e', padx=5)

        entry_invoice = customtkinter.CTkEntry(master=subframe)
        entry_invoice.grid(column=6, row=1, sticky='we', padx=10, pady=7)
        entry_invoice.insert(0, invoiceid)
        entry_invoice.bind('<KeyRelease>', findInvoice)
        entry_invoice.bind("<Up>", on_up_key)
        entry_invoice.bind("<Down>", on_down_key)

        label_cus_name = customtkinter.CTkLabel(master=subframe, text="Nadeera Thilakarathna",
                                                font=("Helvetica", 15, "bold"))
        label_cus_name.grid(column=0, row=1, sticky='w', padx=10, columnspan=1)

        label_cus_data = customtkinter.CTkLabel(master=subframe, justify="left",
                                                text="Kuruwaththa,Pathakada,Pelmadulla\n0710401535\nnadeerathilakarathna4@gmail.com")
        label_cus_data.grid(column=0, row=2, sticky='w', padx=10, columnspan=1)

        label_date = customtkinter.CTkLabel(master=subframe, text="Date", )
        label_date.grid(column=5, row=2, sticky='e', padx=10)

        entry_date = customtkinter.CTkEntry(master=subframe)
        entry_date.grid(column=6, row=2, sticky='we', padx=10, pady=9)

        icon_edit = customtkinter.CTkImage(Image.open("data/icons/edit.png"), size=(20, 20), )
        icon_edit_small = customtkinter.CTkImage(Image.open("data/icons/edit.png"), size=(15, 15), )
        icon_done = customtkinter.CTkImage(Image.open("data/icons/done.png"), size=(20, 20), )
        icon_done_small = customtkinter.CTkImage(Image.open("data/icons/done.png"), size=(15, 15), )
        icon_folder = customtkinter.CTkImage(Image.open("data/icons/location.png"), size=(20, 20), )
        icon_delete = customtkinter.CTkImage(Image.open("data/icons/delete.png"), size=(20, 20), )
        icon_add = customtkinter.CTkImage(Image.open("data/icons/add.png"), size=(20, 20), )
        icon_payment = customtkinter.CTkImage(Image.open("data/icons/payment.png"), size=(20, 20), )

        button_date = customtkinter.CTkButton(master=entry_date, text="", image=icon_edit_small, width=0, height=0,
                                              command=setdate, fg_color=entry_date.cget('fg_color'))
        button_date.grid(column=0, row=0, sticky='e', padx=2)

        label_folder = customtkinter.CTkLabel(master=subframe, text="Directory", )
        label_folder.grid(column=4, row=3, sticky='e', padx=10)

        entry_folder = customtkinter.CTkEntry(master=subframe)
        entry_folder.grid(column=5, columnspan=2, row=3, sticky='we', padx=(10, 50), pady=9)
        entry_folder.bind("<Button-1>", openfolder)

        button_folder = customtkinter.CTkButton(master=subframe, text="", image=icon_folder, width=0,
                                                command=openfolder)
        button_folder.grid(column=6, row=3, sticky='e', padx=10)

        button_edit_folder = customtkinter.CTkButton(master=entry_folder, image=icon_edit_small, text="", width=0,
                                                     height=0,
                                                     fg_color=entry_folder.cget('fg_color'), command=setfolder)
        button_edit_folder.grid(column=0, row=0, sticky='e', padx=2)

        frame_service = customtkinter.CTkScrollableFrame(master=subframe, height=325)
        frame_service.grid(column=0, row=4, columnspan=7, sticky='nesw', padx=10, pady=7)

        frame_add_service = customtkinter.CTkFrame(master=subframe, height=5)
        # frame_add_service.grid(column=0, row=4, columnspan=7, sticky='wes', padx=10,pady=(0,10))

        frame_add_service.columnconfigure(0, weight=1)
        frame_add_service.columnconfigure(1, weight=5)
        frame_add_service.columnconfigure(2, weight=3)
        frame_add_service.columnconfigure(3, weight=2)

        entry_add_jobid = customtkinter.CTkEntry(master=frame_add_service, width=60, placeholder_text='Job ID')
        entry_add_jobid.grid(column=1, row=0, sticky='e', padx=5)

        entry_add_title = customtkinter.CTkEntry(master=frame_add_service, width=300, placeholder_text='Discription')
        entry_add_title.grid(column=2, row=0, sticky='we', padx=5)

        entry_add_price = customtkinter.CTkEntry(master=frame_add_service, width=100, placeholder_text='Price')
        entry_add_price.grid(column=3, row=0, sticky='we', padx=5)

        button_add_service = customtkinter.CTkButton(master=frame_add_service, image=icon_add, text="",
                                                     fg_color=frame_service.cget('fg_color'), width=0,
                                                     command=addservice)
        button_add_service.grid(column=4, row=0, sticky='e', padx=5)

        button_add = customtkinter.CTkButton(subframe, text="", image=icon_add, fg_color=frame_service.cget('fg_color'),
                                             width=0, height=0, command=pressaddservice)
        button_add.grid(column=0, row=4, columnspan=7, sticky='es', padx=30, pady=25)

        label_total = customtkinter.CTkLabel(master=subframe, text="Total: 1250.00", font=("Helvetica", 20, "bold"))
        label_total.grid(column=0, row=6, columnspan=7, padx=10, sticky='e')

        label_amount_paid = customtkinter.CTkLabel(master=subframe, text="Outstanding Balance: 1250.00",)
        label_amount_paid.grid(column=0, row=7, columnspan=7, padx=10, sticky='e')

        button_delete = customtkinter.CTkButton(master=subframe, text="Delete Invoice", image=icon_delete,
                                                command=deleteinvoice)
        button_delete.grid(column=0, row=8, columnspan=2, padx=10, sticky='w')

        button_payment = customtkinter.CTkButton(master=subframe, text="Payments", image=icon_payment,
                                                command=gotopayment)
        button_payment.grid(column=0, row=8, columnspan=7, padx=10, sticky='e')

        f.grab_set()
        findInvoice(invoiceid)
        f.mainloop()


class PaymentDetails:
    def Screen(root):

        def backToHomeScreen():
            gui = Home()
            frame_main.destroy()
            gui.HomeScreen(root=root)

        def load_payment_details(self):
            def printpayment(id):
                p = threading.Thread(target=GenerateReceipt, args=(id,))
                p.start()

            def editpayment(id):
                if (widgets[id]['edit'].cget('image')) == icon_edit:
                    widgets[id]['description'].configure(state='normal', border_width=1)
                    widgets[id]['reference'].configure(state='normal', border_width=1)
                    widgets[id]['date'].configure(state='normal', border_width=1)
                    widgets[id]['amount'].configure(state='normal', border_width=1)
                    widgets[id]['edit'].configure(image=icon_done)
                else:
                    try:
                        if datetime.datetime.strptime(widgets[id]['date'].get(), '%Y-%m-%d'):
                            if (db.UpdatePayment(id, widgets[id]['date'].get(), widgets[id]['reference'].get(),
                                                 widgets[id]['description'].get(), widgets[id]['amount'].get())):
                                widgets[id]['description'].configure(state='readonly', border_width=0)
                                widgets[id]['reference'].configure(state='readonly', border_width=0)
                                widgets[id]['date'].configure(state='disabled', border_width=0)
                                widgets[id]['amount'].configure(state='readonly', border_width=0)
                                widgets[id]['edit'].configure(image=icon_edit)
                                load_payment_details('')
                    except:
                        return False

            def deletepayment(id):
                if db.DeletePayment(id):
                    load_payment_details('')


            payments = db.GetPayments(entry_search.get())
            for w in frame_payment_details.winfo_children():
                w.destroy()
            widgets = {}
            if payments:
                c = 0
                for payment in payments:
                    label_id = customtkinter.CTkLabel(master=frame_payment_details, text=payment[0])
                    label_id.grid(column=0, row=c, padx=10)

                    entry_date = customtkinter.CTkEntry(master=frame_payment_details, width=80, border_width=0)
                    entry_date.grid(column=1, row=c, padx=10)
                    entry_date.insert(0, payment[1])
                    entry_date.configure(state=customtkinter.DISABLED)

                    label_invoice = customtkinter.CTkLabel(master=frame_payment_details, text=payment[2])
                    label_invoice.grid(column=3, row=c, padx=10, sticky='we')

                    label_method = customtkinter.CTkLabel(master=frame_payment_details, text=payment[3])
                    label_method.grid(column=4, row=c, sticky='w', padx=5)

                    entry_reference = customtkinter.CTkEntry(master=frame_payment_details, border_width=0)
                    entry_reference.grid(column=5, row=c, padx=5)
                    entry_reference.insert(0, payment[4])
                    entry_reference.configure(state='readonly')

                    entry_description = customtkinter.CTkEntry(master=frame_payment_details, border_width=0)
                    entry_description.grid(column=6, row=c, padx=5, sticky='we')
                    entry_description.insert(0, payment[5])
                    entry_description.configure(state='readonly')

                    entry_amount = customtkinter.CTkEntry(master=frame_payment_details, justify="right", width=85,
                                                          border_width=0)
                    entry_amount.grid(column=7, row=c, padx=5, pady=10)
                    entry_amount.insert(0, f"{payment[6]:.2f}")
                    entry_amount.configure(state='readonly')

                    button_print = customtkinter.CTkButton(master=frame_payment_details, image=icon_print, width=0,
                                                           height=0,
                                                           fg_color=frame_payment_details.cget('fg_color'), text="",
                                                           command=lambda i=payment: printpayment(i[0]))
                    button_print.grid(column=8, row=c, padx=10)

                    button_edit = customtkinter.CTkButton(master=frame_payment_details, image=icon_edit, width=0,
                                                          height=0, fg_color=frame_payment_details.cget('fg_color'),
                                                          text="", command=lambda i=payment: editpayment(i[0]))
                    button_edit.grid(column=9, row=c, padx=10)

                    button_delete = customtkinter.CTkButton(master=frame_payment_details, image=icon_delete, width=0,
                                                            height=0, fg_color=frame_payment_details.cget('fg_color'),
                                                            text="", command=lambda i=payment: deletepayment(i[0]))
                    button_delete.grid(column=10, row=c, padx=10)

                    elements = {'id': label_id, 'date': entry_date, 'invoice': label_invoice, 'method': label_method,
                                'reference': entry_reference,
                                'description': entry_description, 'amount': entry_amount, 'print': button_print,
                                'edit': button_edit, 'delete': button_delete}

                    widgets[payment[0]] = elements

                    c = c + 1
        def addpayment():
            maxinvoiceid = (db.GetMaxInvoiceID())
            gui = Payment.Screen(root,maxinvoiceid)


        icon_add_payment = customtkinter.CTkImage(Image.open("data/icons/add_payment.png"), size=(20, 20), )
        icon_print = customtkinter.CTkImage(Image.open("data/icons/print.png"), size=(20, 20), )
        icon_edit = customtkinter.CTkImage(Image.open("data/icons/edit.png"), size=(20, 20), )
        icon_delete = customtkinter.CTkImage(Image.open("data/icons/delete.png"), size=(20, 20), )
        icon_done = customtkinter.CTkImage(Image.open("data/icons/done.png"), size=(20, 20), )

        frame_main = customtkinter.CTkFrame(master=root)
        frame_main.pack(pady=20, padx=20, fill="both", expand=True, )

        frame_main.columnconfigure(0, weight=1)

        label_title = customtkinter.CTkLabel(master=frame_main, text="Payment Details")
        label_title.grid(column=0, row=0, pady=10, sticky='we')

        button_home = customtkinter.CTkButton(master=frame_main, text='⌂', command=backToHomeScreen, width=20,
                                              height=20, corner_radius=80)
        button_home.configure(fg_color='transparent')
        button_home.place(x=10, y=10)

        entry_search = customtkinter.CTkEntry(master=frame_main, width=250)
        entry_search.grid(column=0, row=1, pady=5, )
        entry_search.bind('<KeyRelease>', load_payment_details)

        frame_payment_details = customtkinter.CTkScrollableFrame(master=frame_main, height=400)
        frame_payment_details.grid(column=0, row=2, pady=(10, 5), padx=10, sticky='wens')

        button_add_payment = customtkinter.CTkButton(master=frame_main, text="Add Payment", image=icon_add_payment,command=addpayment)
        button_add_payment.grid(column=0, row=3, padx=10, pady=5, sticky='e')

        load_payment_details('')

        frame_payment_details.columnconfigure(5, weight=1, minsize=75)
        frame_payment_details.columnconfigure(6, weight=3, minsize=100)



class Payment():
    def Screen(root,invoiceid):

        def load_payment_details(self):


            def printpayment(id):
                p = threading.Thread(target=GenerateReceipt, args=(id,))
                p.start()

            def editpayment(id):
                if (widgets[id]['edit'].cget('image')) == icon_edit:
                    widgets[id]['description'].configure(state='normal', border_width=1)
                    widgets[id]['reference'].configure(state='normal', border_width=1)
                    widgets[id]['date'].configure(state='normal', border_width=1)
                    widgets[id]['amount'].configure(state='normal', border_width=1)
                    widgets[id]['edit'].configure(image=icon_done)
                else:
                    try:
                        if datetime.datetime.strptime(widgets[id]['date'].get(), '%Y-%m-%d'):
                            if (db.UpdatePayment(id, widgets[id]['date'].get(), widgets[id]['reference'].get(),
                                                 widgets[id]['description'].get(), widgets[id]['amount'].get())):
                                widgets[id]['description'].configure(state='readonly', border_width=0)
                                widgets[id]['reference'].configure(state='readonly', border_width=0)
                                widgets[id]['date'].configure(state='disabled', border_width=0)
                                widgets[id]['amount'].configure(state='readonly', border_width=0)
                                widgets[id]['edit'].configure(image=icon_edit)
                                load_payment_details('')
                    except:
                        return False

            def deletepayment(id):
                if db.DeletePayment(id):
                    load_payment_details('')

            paymentdetails = db.GetDetailsRelatedPayment(entry_invoice.get())
            if (paymentdetails):
                send_combo_method.configure(values=db.GetPaymentMethods().keys())

                label_total.configure(text=fr"Total : {paymentdetails['total']}")
                label_paid.configure(text=fr"Paid : {paymentdetails['paid']}")
                label_to_pay.configure(text=f"To Pay : {paymentdetails['topay']}")
                label_name.configure(text=paymentdetails['customer'])
                label_cus_data.configure(text=paymentdetails['customer_details'])
                label_invoice_details.configure(text=f"{paymentdetails['date']}\nitems : {paymentdetails['items']}")

                send_entry_date.configure(state = customtkinter.NORMAL)
                send_combo_method.configure(state = 'readonly')
                send_button_add_method.configure(state=customtkinter.NORMAL)
                send_entry_price.configure(state=customtkinter.NORMAL)
                send_entry_reference.configure(state=customtkinter.NORMAL)
                send_entry_description.configure(state=customtkinter.NORMAL)
                send_button_add_payment.configure(state=customtkinter.NORMAL)
                button_payment_summary.configure(state=customtkinter.NORMAL)

                if (paymentdetails['topay']<=0):
                    send_combo_method.configure(values=[])
                    send_entry_price.delete(0, customtkinter.END)
                    send_entry_date.delete(0, customtkinter.END)
                    send_entry_date.insert(0, datetime.datetime.now().strftime('%Y-%m-%d'))
                    send_entry_reference.delete(0, customtkinter.END)
                    send_entry_description.delete(0, customtkinter.END)
                    send_entry_date.configure(state=customtkinter.DISABLED)
                    send_combo_method.configure(state=customtkinter.DISABLED)
                    send_button_add_method.configure(state=customtkinter.DISABLED)
                    send_entry_price.configure(state=customtkinter.DISABLED)
                    send_entry_reference.configure(state=customtkinter.DISABLED)
                    send_entry_description.configure(state=customtkinter.DISABLED)
                    send_button_add_payment.configure(state=customtkinter.DISABLED)


                    if (paymentdetails['topay'] == 0):
                        label_paid.configure(text=fr"Payment Success")
                        label_to_pay.configure(text="")


            else:
                label_total.configure(text=fr"Total : ")
                label_paid.configure(text=fr"Paid : ")
                label_to_pay.configure(text=f"To Pay : ")
                label_name.configure(text="")
                label_cus_data.configure(text="")
                label_invoice_details.configure(text=f"\nitems : 0")

                send_combo_method.configure(values=[])
                send_entry_date.configure(state=customtkinter.DISABLED)
                send_combo_method.configure(state=customtkinter.DISABLED)
                send_button_add_method.configure(state=customtkinter.DISABLED)
                send_entry_price.configure(state=customtkinter.DISABLED)
                send_entry_reference.configure(state=customtkinter.DISABLED)
                send_entry_description.configure(state=customtkinter.DISABLED)
                send_button_add_payment.configure(state=customtkinter.DISABLED)
                button_payment_summary.configure(state=customtkinter.DISABLED)

            send_entry_date.delete(0, customtkinter.END)
            send_entry_date.insert(0, datetime.datetime.now().strftime('%Y-%m-%d'))

            send_combo_method_var.set("Payment Method")

            send_entry_price.delete(0, customtkinter.END)
            send_entry_reference.delete(0, customtkinter.END)
            send_entry_description.delete(0, customtkinter.END)

            payments = db.GetPaymentsByInvoice(entry_invoice.get())
            for w in frame_payment_details.winfo_children():
                w.destroy()
            widgets = {}
            if payments:
                c = 0
                for payment in payments:
                    label_id = customtkinter.CTkLabel(master=frame_payment_details, text=payment[0])
                    label_id.grid(column=0, row=c, padx=10)

                    entry_date = customtkinter.CTkEntry(master=frame_payment_details, width=80, border_width=0)
                    entry_date.grid(column=1, row=c, padx=10)
                    entry_date.insert(0, payment[1])
                    entry_date.configure(state=customtkinter.DISABLED)

                    label_method = customtkinter.CTkLabel(master=frame_payment_details, text=payment[3])
                    label_method.grid(column=4, row=c, sticky='w', padx=5)

                    entry_reference = customtkinter.CTkEntry(master=frame_payment_details, border_width=0)
                    entry_reference.grid(column=5, row=c, padx=5)
                    entry_reference.insert(0, payment[4])
                    entry_reference.configure(state='readonly')

                    entry_description = customtkinter.CTkEntry(master=frame_payment_details, border_width=0)
                    entry_description.grid(column=6, row=c, padx=5, sticky='we')
                    entry_description.insert(0, payment[5])
                    entry_description.configure(state='readonly')

                    entry_amount = customtkinter.CTkEntry(master=frame_payment_details, justify="right", width=85,
                                                          border_width=0)
                    entry_amount.grid(column=7, row=c, padx=5, pady=10)
                    entry_amount.insert(0, f"{payment[6]:.2f}")
                    entry_amount.configure(state='readonly')

                    button_print = customtkinter.CTkButton(master=frame_payment_details, image=icon_print, width=0,
                                                           height=0,
                                                           fg_color=frame_payment_details.cget('fg_color'), text="",
                                                           command=lambda i=payment: printpayment(i[0]))
                    button_print.grid(column=8, row=c, padx=10)

                    button_edit = customtkinter.CTkButton(master=frame_payment_details, image=icon_edit, width=0,
                                                          height=0, fg_color=frame_payment_details.cget('fg_color'),
                                                          text="", command=lambda i=payment: editpayment(i[0]))
                    button_edit.grid(column=9, row=c, padx=10)

                    button_delete = customtkinter.CTkButton(master=frame_payment_details, image=icon_delete, width=0,
                                                            height=0, fg_color=frame_payment_details.cget('fg_color'),
                                                            text="", command=lambda i=payment: deletepayment(i[0]))
                    button_delete.grid(column=10, row=c, padx=10)

                    elements = {'id': label_id, 'date': entry_date, 'invoice': label_invoice, 'method': label_method,
                                'reference': entry_reference,
                                'description': entry_description, 'amount': entry_amount, 'print': button_print,
                                'edit': button_edit, 'delete': button_delete}

                    widgets[payment[0]] = elements
                    c = c + 1

        def addpayment():
            def is_valid_date(date_string):
                try:
                    datetime.datetime.strptime(date_string, '%Y-%m-%d')
                    return True
                except ValueError:
                    return False

            if (bool(label_name.cget('text'))):
                if is_valid_date(send_entry_date.get()):

                    if (send_entry_price.get().isdigit() and entry_invoice.get().isdigit() and (send_combo_method_var.get() in db.GetPaymentMethods().keys())):
                        #print("T")
                        payment_methods = db.GetPaymentMethods()
                        if (db.AddPayment(send_entry_date.get(),entry_invoice.get(),payment_methods[send_combo_method_var.get()],send_entry_reference.get(),send_entry_description.get(),send_entry_price.get())):
                            load_payment_details('')
                        else:
                            send_entry_price.focus()


        def addpaymentmethod():
            def addmethod():
                if((entry_method.get())):
                    if (db.AddPaymentMethod(entry_method.get())):
                        load_payment_details('')
                        main.destroy()
            main = customtkinter.CTkToplevel(frame_main)
            main.title("Add Payment Method")  # set the window title
            main.iconbitmap("data/icon.ico")

            width = 400 ;height = 200

            x = (main.winfo_screenwidth() / 2) - (width / 2)
            y = (main.winfo_screenheight() / 2) - (height / 2)

            main.geometry('%dx%d+%d+%d' % (width, height, x + 100, y - 40))

            entry_method = customtkinter.CTkEntry(master=main,width=300)
            entry_method.grid(column=0,row=0,pady=(50,10),padx=10)

            button_method = customtkinter.CTkButton(master=main,width=100,text="Add Method",image=icon_add,command=addmethod)
            button_method.grid(column=0,row=1,pady=10,padx=10)

            main.columnconfigure(0,weight=1)
            main.resizable(False, False)

            main.grab_set()

        def paymentsummary():
            if bool(label_name.cget('text')):
                p = threading.Thread(target=GeneratePaymentSummary, args=(entry_invoice.get(),))
                p.start()

        def on_up_key(event):
            current_value = entry_invoice.get()
            if current_value.isdigit():
                new_value = int(current_value) + 1
                entry_invoice.delete(0, customtkinter.END)
                entry_invoice.insert(0, new_value)

        def on_down_key(event):
            current_value = entry_invoice.get()
            if current_value.isdigit() and int(current_value) > 1:
                new_value = int(current_value) - 1
                entry_invoice.delete(0, customtkinter.END)
                entry_invoice.insert(0, new_value)



        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        frame_main = customtkinter.CTkToplevel(root)
        # f.attributes('-topmost', 'true')

        frame_main.title("Payment")  # set the window title
        frame_main.iconbitmap("data/icon.ico")

        width = 1000  # Width
        height = 600  # Height

        screen_width = frame_main.winfo_screenwidth()  # Width of the screen
        screen_height = frame_main.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        icon_add = customtkinter.CTkImage(Image.open("data/icons/add.png"), size=(20, 20), )
        icon_add_payment = customtkinter.CTkImage(Image.open("data/icons/add_payment.png"), size=(20, 20), )
        icon_print = customtkinter.CTkImage(Image.open("data/icons/print.png"), size=(20, 20), )
        icon_edit = customtkinter.CTkImage(Image.open("data/icons/edit.png"), size=(20, 20), )
        icon_delete = customtkinter.CTkImage(Image.open("data/icons/delete.png"), size=(20, 20), )
        icon_done = customtkinter.CTkImage(Image.open("data/icons/done.png"), size=(20, 20), )
        icon_print = customtkinter.CTkImage(Image.open("data/icons/print.png"), size=(20, 20), )

        frame_main.geometry('%dx%d+%d+%d' % (width, height, x + 50, y - 40))

        frame_main.columnconfigure(0,weight=1)
        frame_main.rowconfigure(0, weight=1)

        frame_sub = customtkinter.CTkFrame(master=frame_main)
        frame_sub.grid(column=0,row=0,sticky='nswe',padx=10,pady=10)

        frame_sub.columnconfigure(0,weight=1)

        label_main_title = customtkinter.CTkLabel(master=frame_sub, text="Payment")
        label_main_title.grid(column=0, row=0, sticky='we', columnspan=7, pady=10)

        label_name = customtkinter.CTkLabel(master=frame_sub, text='Nadeera Thilakarathna',font=("Helvetica", 15, "bold"),justify='left')
        label_name.grid(column=0, row=1,padx=10,sticky='w')

        label_cus_data = customtkinter.CTkLabel(master=frame_sub, text='Pelmadulla\n0710401535\nnadeerathilakarathna4@gmail.com',justify='left')
        label_cus_data.grid(column=0, row=2, padx=10,sticky='w')

        frame_sub.rowconfigure(2,minsize=80)

        label_invoice = customtkinter.CTkLabel(master=frame_sub,text='Invoice',)
        label_invoice.grid(column=3, row=1, padx=5,sticky='e')

        entry_invoice = customtkinter.CTkEntry(master=frame_sub,width=200)
        entry_invoice.insert(0,invoiceid)
        entry_invoice.grid(column=4, row=1, padx=10,sticky='e')
        entry_invoice.bind('<KeyRelease>', load_payment_details)
        entry_invoice.bind("<Up>", on_up_key)
        entry_invoice.bind("<Down>", on_down_key)

        label_invoice_details = customtkinter.CTkLabel(master=frame_sub, text='items: 10',justify='right')
        label_invoice_details.grid(column=4, row=2, padx=10, sticky='e')

        frame_payment_details = customtkinter.CTkScrollableFrame(master=frame_sub, height=150)
        frame_payment_details.grid(column=0, row=3, pady=(10, 5), padx=10, sticky='wens',columnspan = 5)



        frame_payment_details.columnconfigure(5, weight=1)
        frame_payment_details.columnconfigure(6, weight=1)


        label_total = customtkinter.CTkLabel(master=frame_sub, text="Total : 3000.00",font=("Helvetica", 20, "bold"))
        label_total.grid(column=0, row=4, padx=10, sticky='w')

        label_paid = customtkinter.CTkLabel(master=frame_sub, text="Paid : 2000.00", font=("Helvetica", 20,))
        label_paid.grid(column=4, row=4, padx=10, sticky='e')

        label_to_pay = customtkinter.CTkLabel(master=frame_sub, text="To Paid : 1000.00", font=("Helvetica", 18,))
        label_to_pay.grid(column=4, row=5, padx=10, sticky='e')

        frame_add_payment = customtkinter.CTkFrame(master=frame_sub,fg_color=frame_sub.cget('fg_color'))
        frame_add_payment.grid(column=0,row=6,columnspan=5,padx=(10,0))



        send_entry_date = customtkinter.CTkEntry(master=frame_add_payment,width=200,placeholder_text="Date")
        send_entry_date.insert(0, datetime.datetime.now().strftime('%Y-%m-%d'))
        send_entry_date.grid(column=0, row=0, padx=5, sticky='w',pady=5)

        send_combo_method_var = customtkinter.StringVar(value="Payment Method")
        color_frame_sub = send_entry_date.cget('fg_color')
        send_combo_method = customtkinter.CTkComboBox(master=frame_add_payment,values=["BOC Account", "Cash","Peoples Bank"],variable=send_combo_method_var,bg_color=color_frame_sub,fg_color=color_frame_sub,state='readonly')
        send_combo_method.grid(column=1,row=0,padx=(5,35),)

        send_button_add_method = customtkinter.CTkButton(master=frame_add_payment,text="",image=icon_add,width=0,height=0,fg_color=frame_sub.cget('fg_color'),command=addpaymentmethod)
        send_button_add_method.grid(column=1,row=0,padx=5,sticky='e')

        send_entry_price = customtkinter.CTkEntry(master=frame_add_payment, width=200,placeholder_text='Price')
        send_entry_price.grid(column=2, row=0, padx=5, sticky='we')

        send_entry_reference = customtkinter.CTkEntry(master=frame_add_payment, width=200, placeholder_text='Reference')
        send_entry_reference.grid(column=0, row=1, padx=5, sticky='we')

        send_entry_description = customtkinter.CTkEntry(master=frame_add_payment, width=200, placeholder_text='Description')
        send_entry_description.grid(column=1, row=1, padx=5, sticky='we',columnspan=2,pady=10)

        send_button_add_payment = customtkinter.CTkButton(master=frame_add_payment,text="Add Payment",image=icon_add_payment,command=addpayment)
        send_button_add_payment.grid(column=3,row=0,rowspan=2,sticky='ns',padx=10,pady=10)

        button_payment_summary = customtkinter.CTkButton(master=frame_sub, text="Payment Summary",height=30, image=icon_print,command=paymentsummary)
        button_payment_summary.grid(column=0, row=7,columnspan=5, padx=10, pady=10)

        frame_add_payment.columnconfigure(0, weight=1)
        frame_add_payment.columnconfigure(1,weight=1)
        frame_add_payment.columnconfigure(2, weight=1)

        frame_main.grab_set()

        load_payment_details("")







