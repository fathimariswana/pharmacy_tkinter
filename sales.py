import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import mysql.connector
from docxtpl import DocxTemplate
import datetime

window = Tk()

def sales():
    sl=1
    ds = start_date.get()
    es = end_date.get()
    medlist = []
    invoiceli = []
    sub_tot = 0
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_obj = db_obj.cursor()
    sql = "SELECT DISTINCT medname FROM bill_info WHERE date_gen BETWEEN '"+ds+"' AND '"+es+"'"
    sql_obj.execute(sql)
    mednames = sql_obj.fetchall()
    for i in mednames:
        medlist.append(i[0])
    for i in medlist:
        sql_tot = "SELECT medname, quantity, total FROM bill_info WHERE medname='"+i+"' AND date_gen BETWEEN '"+ds+"' AND '"+es+"'"
        sql_obj.execute(sql_tot)
        tot_med= sql_obj.fetchall()
        total=0
        qty_total = 0
        for i in tot_med:
            mednm = i[0]
            total = total+float(i[2])
            qty_total = qty_total+int(i[1])
            sub_tot = sub_tot+float(i[2])
        invoice_list = [sl, mednm, qty_total, total]
        sl = sl+1
        invoiceli.append(invoice_list)
        table.insert("", tk.END, values=(invoice_list[1],invoice_list[2], invoice_list[3]))
    db_obj.commit()
    db_obj.close()
    style = ttk.Style()
    style.theme_use('clam')
    table.heading(1, text="Medicine Name")
    table.column(1, anchor='n')
    table.heading(2, text="Quantity")
    table.column(2, anchor='n')
    table.heading(3, text="Total Price")
    table.column(3, anchor='n')
    table.grid(row=3, column=1, columnspan=3, padx=10, pady=10)
    total_sale=IntVar()
    sale_lbl = Label(salesframe, text="Total sales", font=('Times 14'))
    sale_lbl.grid(row=4, column=1, pady=10, padx=10)
    sales_entry = Entry(salesframe, font=('Times 14'), width=20, textvariable=total_sale)
    sales_entry.grid(row=4, column=2)
    total_sale.set(sub_tot)
    Now = datetime.datetime.now()
    dategen = Now.date()
    doc = DocxTemplate("sales.docx")
    doc.render({"dategen": dategen, "invoice_list": invoiceli, "sub_tot": sub_tot})
    doc.save("newSales.docx")

window.title('Sales report generator')
salesframe = LabelFrame(window, text='Sales Check', font=('Times 14'), background="#96e0e0")
salesframe.pack(padx=10, pady=10, fill='both')
start_label = Label(salesframe, text="Select Start Date", font=('Times 14'))
start_label.grid(row=0, column=1, pady=10, padx=10)
start_date = DateEntry(salesframe, width= 16, background= "magenta3", foreground= "white",bd=2, date_pattern='YYYY-MM-DD')
start_date.grid(row=0, column=2,pady=10, padx=10)
end_label=Label(salesframe, text="Select End Date", font=('Times 14'))
end_label.grid(row=1,column=1, pady=10, padx=10)
end_date = DateEntry(salesframe, width= 16, background= "magenta3", foreground= "white",bd=2, date_pattern='YYYY-MM-DD')
end_date.grid(row=1,column=2, pady=10, padx=10)
btn_sales=Button(salesframe, text="Generate Sales Report", font=('Times 14'), background='black', foreground='white', command=sales)
btn_sales.grid(row=2, column=1, columnspan=2, pady=10, padx=10)
table = ttk.Treeview(salesframe, columns=(1,2,3), show="headings")

window.mainloop()