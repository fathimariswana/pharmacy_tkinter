from tkinter import *
from docxtpl import DocxTemplate
import tkinter as tk
from tkinter import ttk
import mysql.connector
import random
import datetime
from tkinter import messagebox
Now = datetime.datetime.now()
dt = Now.date()
rad = random.randint(1000, 20000)
val =str(rad)
window = Tk()
window.title("Generate Bill")
invoice_lf = LabelFrame(window, text='Bill Generator', font=('Times 14'))
invoice_lf.pack(padx=10, pady=10, fill='both')
invoiceNumber = IntVar()
med_name = StringVar()
global comp_name
comp_name = StringVar()
global quantity
quantity =IntVar()
global price_unit
price_unit = IntVar()
global rack
rack = StringVar()
def getrow(event):
    row_id = invoice_table.identify_row(event.y)
    item = invoice_table.item(invoice_table.focus())
    comp=item['values'][6]
    med_name.set(item['values'][1])
    quantity.set(item['values'][2])
    price_unit.set(item['values'][3])
    rack.set(item['values'][5])
    comp_name.set('')
    comp_name.set(comp)
def update(rows):
    invoicenum = invoiceNumber.get()
    invoice_table.delete(*invoice_table.get_children())
    for i in rows:
        invoice_table.insert('', tk.END, values=(invoicenum, i[0], i[1], i[2], i[3], i[4], i[5]))
def clear():
    invoicenum = invoiceNumber.get()
    invnm = str(invoicenum)
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_obj = db_obj.cursor()
    query = "SELECT medname, quantity, price, total, rack, compname FROM bill_info WHERE invoice_num="+invnm
    sql_obj.execute(query)
    rows = sql_obj.fetchall()
    db_obj.commit()
    db_obj.close()
    update(rows)
def search():
   clear()
def generate_invoice():
    cstname = name.get()
    cstphn = phone.get()
    dategen = date_gen.get()
    invoice_list=[]
    invoicenum = invoiceNumber.get()
    invoiceno = str(invoicenum)
    sl = 1
    sub_tot = 0
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_obj = db_obj.cursor()
    query = "SELECT * FROM bill_info WHERE invoice_num=" + invoiceno
    sql_obj.execute(query)
    rows = sql_obj.fetchall()
    for i in rows:
        cstname = i[3]
        cstphn=i[2]
        med_nm = i[4]
        quantty = i[5]
        unit_pr = i[6]
        tot = i[7]
        dategen = i[1]
        rak = i[8]
        item =[sl, med_nm, quantty, unit_pr, tot]
        invoice_list.append(item)
        sub_tot = sub_tot+float(tot)
        sl=sl+1
        cmp = i[9]
        sql_quantity_fetch= "SELECT qty FROM stocklist WHERE medname='"+med_nm+"' AND compname='"+cmp+"' AND rack='"+rak+"'"
        sql_obj.execute(sql_quantity_fetch)
        quantity_stock = sql_obj.fetchall()
        for i in quantity_stock:
            qt = i[0]
        quantity = int(qt)-int(quantty)
        qt_y =str(quantity)
        sql_update_stock = "UPDATE stocklist SET qty="+qt_y+" WHERE medname='"+med_nm+"' AND compname='"+cmp+"' AND rack='"+rak+"'"
        sql_obj.execute(sql_update_stock)
    db_obj.commit()
    db_obj.close()
    doc = DocxTemplate("invoice.docx")
    doc.render({"cstname": cstname, "cstphn": cstphn,"dategen":dategen, "invoiceno": invoiceno, "invoice_list": invoice_list, "subtotal":sub_tot})
    doc.save("newInvoice.docx")
def update_item():
    invoicenum = invoiceNumber.get()
    qt = int(quantity.get())
    invnm = str(invoicenum)
    medicineNm = med_name.get()
    rate = float(price_unit.get())
    tot = qt * rate
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_obj = db_obj.cursor()
    query = "UPDATE bill_info SET quantity=%s, price=%s, total=%s WHERE invoice_num=%s AND medname=%s"
    sql_obj.execute(query, (qt, rate, tot, invnm, medicineNm))
    db_obj.commit()
    db_obj.close()
    clear()
def delete_item():
    invoicenum = invoiceNumber.get()
    qt = str(quantity.get())
    invnm = str(invoicenum)
    medicineNm = med_name.get()
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_obj = db_obj.cursor()
    if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete the record?"):
        query = "DELETE FROM bill_info WHERE invoice_num="+invnm+" AND medname='"+medicineNm+"' AND quantity="+qt
        sql_obj.execute(query)
        db_obj.commit()
        db_obj.close()
        clear()
    else:
        return True
    clear()
def add_invoice():
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_obj = db_obj.cursor()
    cmp_name = comp_name.get()
    rak = rack.get()
    qt = int(quantity.get())
    rate = float(price_unit.get())
    tot = qt * rate
    invoicenum=invoiceNumber.get()
    date = date_gen.get()
    cst_name = name.get()
    cst_phone = phone.get()
    medicineName = med_name.get()
    sql_qty = "SELECT qty FROM stockList WHERE compname='" + cmp_name + "' AND medname='" + medicineName + "'"
    sql_obj.execute(sql_qty)
    item_price = sql_obj.fetchall()
    total_quantity=0
    for i in item_price:
        total_quantity=int(i[0])
    print(total_quantity, qt)
    if qt < total_quantity:
        sql_add = "INSERT INTO bill_info(invoice_num, date_gen, phone_num, name, medname, quantity, price, total, rack, compname) " \
                  "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (invoicenum, date, cst_phone, cst_name, medicineName, qt, rate, tot, rak, cmp_name)
        sql_obj.execute(sql_add, values)
        db_obj.commit()
        db_obj.close()
        clear()
    else:
        messagebox.showerror('error', 'Out of stock')

def get_price():
    priceli = []
    rackli=[]

    cmp_name = comp_name.get()
    medicineName = med_name.get()
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_obj = db_obj.cursor()
    sql_price = "SELECT price,rack,qty FROM stockList WHERE compname='"+cmp_name+"' AND medname='"+medicineName+"'"
    sql_obj.execute(sql_price)
    item_price = sql_obj.fetchall()
    for i in item_price:
        priceli.append(i[0])
        rackli.append(i[1])

    rack_lbl = Label(invoice_lf, text='Rack#:', font=('Times 14'))
    rack_lbl.grid(row=2, column=7, padx=5, pady=5)
    racknum = ttk.Combobox(invoice_lf, values=rackli, textvariable=rack)
    racknum.grid(row=2, column=8)
    racknum.set("Select One")
    # 3rd row widgets including unit price
    qty_lbl = Label(invoice_lf, text='Quantity', font=('Times 14'))
    qty_lbl.grid(row=3, column=1, padx=10, pady=10)
    qty = ttk.Spinbox(invoice_lf, from_=1, to=100, textvariable=quantity)
    qty.grid(row=3, column=2, padx=10, pady=10)
    unit_price_lbl = Label(invoice_lf, text='Unit Price', font=('Times 14'))
    unit_price_lbl.grid(row=3, column=3, padx=10, pady=10)
    unit_price = ttk.Combobox(invoice_lf, values=priceli, textvariable=price_unit)
    unit_price.grid(row=3, column=4, padx=10, pady=10)
    unit_price.set("Select Price")
    add_btn = Button(invoice_lf, text='Add Item', font=('Times 14'), width=10,
                     background='green', foreground='white', command=add_invoice)
    add_btn.grid(row=3, column=5, pady=10, padx=10)

    del_btn = Button(invoice_lf, text='Delete Item', font=('Times 14'), width=10,
                     background='red', foreground='white', command=delete_item)
    del_btn.grid(row=3, column=6, padx=10, pady=10)

    update_btn = Button(invoice_lf, text='Update Item', font=('Times 14'), width=10,
                        background='blue', foreground='white', command=update_item)
    update_btn.grid(row=3, column=7, pady=10, padx=10)

def check_company():
    companyli = []
    medicineNm = med_name.get()
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_obj = db_obj.cursor()
    sql_company = "SELECT compname FROM stockList WHERE medname='"+medicineNm+"'"
    sql_obj.execute(sql_company)
    items_company = sql_obj.fetchall()
    for i in items_company:
        companyli.append(i)
    company_lable = Label(invoice_lf, text='Company Name:', font=('Times 14'))
    company_lable.grid(row=2, column=4, pady=10, padx=10)
    company_name = ttk.Combobox(invoice_lf, values=companyli, textvariable=comp_name)
    company_name.grid(row=2, column=5, padx=10, pady=10)
    company_name.set("Select One")
    check_price = Button(invoice_lf, text='Find Unit Price', background='black', foreground='white', font=('Times 14'),
                         command=get_price)
    check_price.grid(row=2, column=6, pady=10, padx=10)
    db_obj.commit()
    db_obj.close()

medicine_list = []
db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
sql_obj = db_obj.cursor()
sql = "SELECT * FROM medicine"
sql_obj.execute(sql)
items_medicine = sql_obj.fetchall()
for i in items_medicine:
    medicine_list.append(i[1])
db_obj.commit()
db_obj.close()

# first row
invoice = Label(invoice_lf, text='Invoice#:', font=('Times 14'), width=20)
invoice.grid(row=0, column=1, padx=10, pady=10)
invoice_num = Entry(invoice_lf, width=20, textvariable=invoiceNumber)
invoice_num.grid(row=0, column=2, padx=10, pady=10)
invoiceNumber.set(rad)
date_gen_lbl = Label(invoice_lf, text='Date:', font=('Times 14'), width=20)
date_gen_lbl.grid(row=0, column=3, padx=10, pady=10)
date_gen = Entry(invoice_lf, width=20)
date_gen.grid(row=0, column=4, padx=10, pady=10)
date_gen.insert(0, dt)
name_lbl = Label(invoice_lf, text='Name:', font=('Times 14'), width=20)
name_lbl.grid(row=0, column=5, padx=10, pady=10)
name = Entry(invoice_lf, width=20)
name.grid(row=0, column=6, padx=10, pady=10)
phone_lbl = Label(invoice_lf, text='Phone#:', font=('Times 14'), width=20)
phone_lbl.grid(row=0, column=7, padx=10, pady=10)
phone = Entry(invoice_lf, width=20)
phone.grid(row=0, column=8, padx=10, pady=10)
# second row
medname_label = Label(invoice_lf, text="Medicine Name", font=('Times 14'))
medname_label.grid(row=2, column=1, padx=10, pady=10)
medname = ttk.Combobox(invoice_lf, values=medicine_list, textvariable=med_name)
medname.grid(row=2, column=2, padx=10, pady=10)
medname.set('Select One')
check_company_btn = Button(invoice_lf, text="Check Company", command=check_company, font=('Times 14'),
                           background='black', foreground='white')
check_company_btn.grid(row=2, column=3, padx=10, pady=10)


search_btn = Button(invoice_lf, text='Search Invoice', font=('Times 14'), width=10,
                        background='yellow', foreground='black', command=search)
search_btn.grid(row=3, column=8, pady=10, padx=10)

# table view
style = ttk.Style()
style.theme_use('clam')
invoice_table = ttk.Treeview(invoice_lf, columns=(1, 2, 3, 4, 5,6,7), show='headings')
invoice_table.grid(row=6, column=1, columnspan=8, padx=10, pady=10)
invoice_table.configure(selectmode='extended')
invoice_table.heading(1, text='Invoice#')
invoice_table.heading(2, text='Particular')
invoice_table.heading(3, text='Qty')
invoice_table.heading(4, text='Unit Price')
invoice_table.heading(5, text='Amount')
invoice_table.heading(6, text='Rack#')
invoice_table.heading(7, text='Company name')
# on click listener

invoice_table.bind('<Double 1>', getrow)

gen_invoice = Button(invoice_lf, text="Generate Invoice", command=generate_invoice, font=('Times 14'),
                        background='black', foreground='white', width=100)
gen_invoice.grid(row=8, column=1, columnspan=8, padx=10, pady=10)
window.mainloop()