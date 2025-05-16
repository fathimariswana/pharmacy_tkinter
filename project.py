import tkinter as tk
from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import os


window = Tk()
window.title('Pharmacy Management System')

heading = LabelFrame(window)
heading.pack(fill='both', padx=20, pady=10)
title = Label(heading, text="PHARMACY MANAGEMENT SYSTEM", font='100', height=2)
title.pack()

# stock frame
stockFrame = LabelFrame(window, text='Medicine Management Profile', font=('Times 14'))
stockFrame.pack(side=tk.LEFT, expand=1, padx=10, pady=10, fill='both')

# medicine frame
medFrame = LabelFrame(window, text='Medicine Profile', font=('Times 14'),width=100)
medFrame.pack(pady=10, padx=10, fill='both', side=tk.RIGHT)

# medicine list frame and table
medListFrame = LabelFrame(medFrame)
medListFrame.grid(row=7, column=1, columnspan=6, padx=5, pady=10)
medtable = ttk.Treeview(medListFrame, columns = (1,2), show= "headings")

# stock table intialization
stocktable = ttk.Treeview(stockFrame, columns=(1,2,3,4,5,6,7,8,9,10,11,12), show="headings")
stocktable.grid(row=20, columnspan=20, pady=2, padx=2)

# medicine profile db code
medreferance = StringVar()
medicinename = StringVar()
def med_insert():
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_obj = db_obj.cursor()
    refno = medreferance.get()
    mednm = medicinename.get()
    # sql = "CREATE TABLE medicine(ref_id char(20) primary key, medname char(20))"
    if refno != "" and mednm != "":
        if messagebox.askyesno("Are you sure?", "Are you sure you want to insert the new medicine record?"):
            sql = "INSERT INTO medicine (ref_id, medname) VALUES(%s, %s)"
            values = (refno, mednm)
            sql_obj.execute(sql, values)
            db_obj.commit()
            db_obj.close()
            messagebox.showinfo('info', 'record inserted successfully')
            medreferance.set("")
            medicinename.set("")
            med_clear()
        else:
            return True
    else:
        messagebox.showerror('Error', 'fields are empty')

def view_med(rows):
    medtable.delete(*medtable.get_children())
    for i in rows:
        medtable.insert('', tk.END, values=i)

def getrow(event):
    row_id = medtable.identify_row(event.y)
    item = medtable.item(medtable.focus())
    medreferance.set(item['values'][0])
    medicinename.set(item['values'][1])

def med_clear():
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_db = db_obj.cursor()
    sql = "SELECT * FROM medicine"
    sql_db.execute(sql)
    row_out = sql_db.fetchall()
    view_med(row_out)
    db_obj.commit()
    db_obj.close()

def med_delete():
    if messagebox.askyesno('delete?', 'Are you sure you want to delete?'):
        id = medreferance.get()
        db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
        sql_obj = db_obj.cursor()
        sql = "DELETE FROM medicine WHERE ref_id="+id
        sql_obj.execute(sql)
        db_obj.commit()
        db_obj.close()
        med_clear()
        medreferance.set("")
        medicinename.set("")
        messagebox.showinfo('Success', 'Record deleted successfully')
    else:
        return True

def med_update():
    if messagebox.askyesno('Update?', 'Are you do you want to update?'):
        ref = medreferance.get()
        mnm = medicinename.get()
        db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
        sql_obj = db_obj.cursor()
        sql = "UPDATE medicine SET ref_id=%s, medname=%s WHERE ref_id=%s"
        sql_obj.execute(sql, (ref, mnm, ref))
        db_obj.commit()
        db_obj.close()
        med_clear()
        messagebox.askyesno('Success', 'Item updated successfully')
        medicinename.set("")
        medreferance.set("")
    else:
        return True
medlist = []
db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
sql_db = db_obj.cursor()
sql = "SELECT * FROM medicine "
sql_db.execute(sql)
row_out = sql_db.fetchall()
for i in row_out:
    medlist.append(i[1])
view_med(row_out)
db_obj.commit()
db_obj.close()

cmpNam= StringVar()
medotyp = StringVar()
issDt = StringVar()
expDt = StringVar()
uss = StringVar()
sdEff = StringVar()
dos = StringVar()
rate = StringVar()
qty = StringVar()
rak = StringVar()

# stock list db actions
def stock_insert():
    # rn = refnum.get()
    cn = compname.get()
    mn = medName.get()
    mt = medtype.get()
    idt = issueDate.get()
    exdt = expDate.get()
    uss = uses.get()
    se = sideEffect.get()
    dos = dosage.get()
    pr = price.get()
    qt = quantity.get()
    rk = rack.get()
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_obj = db_obj.cursor()
    '''sql = "CREATE TABLE stockList (ref_id char(20), compname char(20), medname char(20), typoMed char(20), issueDate DATE, expDate DATE," \
          "uses char(20), sideEff char(20), dos char(20), price decimal(10,2), qty char(20), rack char(20))"'''
    sql_refid = "SELECT ref_id FROM medicine WHERE medname='"+mn+"'"
    sql_obj.execute(sql_refid)
    item = sql_obj.fetchall()
    for i in item:
        ref = i[0]
    sql = "INSERT INTO stockList (ref_id, compname, medname, typoMed, issueDate, expDate, uses, sideEff, dos, price, qty, rack) VALUES(%s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)"
    values = (ref, cn, mn, mt, idt, exdt, uss, se, dos, pr, qt, rk)
    sql_obj.execute(sql, values)
    db_obj.commit()
    db_obj.close()
    stock_clear()
    messagebox.showinfo('Success', 'Inserted the stock successfully')
    reset()

def view_stock(rows):
    stocktable.delete(*stocktable.get_children())
    for i in rows:
        stocktable.insert('', tk.END, values=i)
def stock_clear():
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_db = db_obj.cursor()
    sql = "SELECT * FROM stockList"
    sql_db.execute(sql)
    row_out = sql_db.fetchall()
    view_stock(row_out)
    db_obj.commit()
    db_obj.close()

def getrowstock(event):
    row_id = stocktable.identify_row(event.y)
    item = stocktable.item(stocktable.focus())
    # refnum.set(item['values'][0])
    cmpNam.set(item['values'][1])
    medName.set(item['values'][2])
    medotyp.set(item['values'][3])
    issDt.set(item['values'][4])
    expDt.set(item['values'][5])
    uss.set(item['values'][6])
    sdEff.set(item['values'][7])
    dos.set(item['values'][8])
    rate.set(item['values'][9])
    qty.set(item['values'][10])
    rak.set(item['values'][11])

def stock_delete():
    id = refnum.get()
    if id == "Select One":
        messagebox.showinfo('Error', 'Fields cannot be empty')
    else:
        db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
        sql_obj = db_obj.cursor()
        sql = 'DELETE FROM stockList WHERE ref_id='+id
        sql_obj.execute(sql)
        db_obj.commit()
        db_obj.close()
        stock_clear()
        messagebox.showinfo("Success", 'Item Deleted Successfully')
        reset()
def reset():
    cmpNam.set("")
    medName.set("Select One")
    medotyp.set("")
    issDt.set("YYYY-MM-DD")
    expDt.set("YYYY-MM-DD")
    uss.set("")
    sdEff.set("")
    dos.set("")
    rate.set("")
    qty.set("")
    rak.set("")
def stock_update():
    rn = refnum.get()
    cn = compname.get()
    mn = medName.get()
    mt = medtype.get()
    idt = issueDate.get()
    exdt = expDate.get()
    uss = uses.get()
    se = sideEffect.get()
    dos = dosage.get()
    pr = price.get()
    qt = quantity.get()
    rk = rack.get()
    db_obj = mysql.connector.connect(host='localhost', user='root', password="", database='pharmacy')
    sql_obj = db_obj.cursor()
    sql = "UPDATE stockList SET ref_id =%s, compname=%s, medname=%s, typoMed=%s, issueDate=%s, expDate=%s, uses=%s, sideEff=%s, dos=%s, price=%s, qty=%s, rack=%s"
    sql_obj.execute(sql, (rn, cn, mn, mt, idt, exdt, uss, se, dos, pr, qt, rk))
    db_obj.commit()
    db_obj.close()
    reset()
    stock_clear()
    messagebox.showinfo('Success', 'Stock Updated Successfully')

def search_med():
    mednm = searchbx.get()
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_obj = db_obj.cursor()
    sql = "SELECT * FROM stocklist WHERE medname='"+mednm+"'"
    sql_obj.execute(sql)
    item = sql_obj.fetchall()
    db_obj.commit()
    db_obj.close()
    view_stock(item)

def reset_table():
    db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
    sql_obj = db_obj.cursor()
    sql = "SELECT * FROM stocklist"
    sql_obj.execute(sql)
    item = sql_obj.fetchall()
    db_obj.commit()
    db_obj.close()
    view_stock(item)
db_obj = mysql.connector.connect(host="localhost", user="root", password="", database="pharmacy")
sql_db = db_obj.cursor()
sql = "SELECT * FROM stockList "
sql_db.execute(sql)
row_out = sql_db.fetchall()
view_stock(row_out)
db_obj.commit()
db_obj.close()

# stock

medLabel = Label(stockFrame, text='Medicine Name', font=('Times 14'), width=20)
medLabel.grid(row=3, column=1)
medName = ttk.Combobox(stockFrame, width=40, values=medlist)
medName.grid(row=3, column=2)
medName.set("Select One")

compLabel = Label(stockFrame, text='Company Name', font=('Times 14'), width=20)
compLabel.grid(row=4, column=1)
compname = Entry(stockFrame, width=43, textvariable=cmpNam)
compname.grid(row=4, column=2)

typelabel = Label(stockFrame, text='Type of Medicine', font=('Times 14'), width=20)
typelabel.grid(row=5, column=1)
medtype = Entry(stockFrame, width=43, textvariable=medotyp)
medtype.grid(row=5, column=2)
issueLabel = Label(stockFrame, text='Issue Date', font=('Times 14'), width=20)
issueLabel.grid(row=6, column=1)
issueDate = Entry(stockFrame, width=43, textvariable=issDt)
issueDate.grid(row=6, column=2)
issDt.set('YYYY-MM-DD')
expLabel = Label(stockFrame, text='Expiry Date', font=('Times 14'), width=20)
expLabel.grid(row=7, column=1)
expDate = Entry(stockFrame, width=43, textvariable=expDt)
expDate.grid(row=7, column=2)
expDt.set('YYYY-MM-DD')
usesLabel = Label(stockFrame, text='Uses', font=('Times 14'), width=20)
usesLabel.grid(row=8, column=1)
uses = Entry(stockFrame,width=43, textvariable=uss)
uses.grid(row=8, column=2)
sideLabel = Label(stockFrame, text='Side Effect', font=('Times 14'), width=20)
sideLabel.grid(row=9, column=1)
sideEffect = Entry(stockFrame, width=43, textvariable=sdEff)
sideEffect.grid(row=9, column=2)
dosLabel = Label(stockFrame, text='Dosage', font=('Times 14'), width=20)
dosLabel.grid(row=10, column=1)
dosage = Entry(stockFrame, width=43, textvariable=dos)
dosage.grid(row=10, column=2)
priceLabel = Label(stockFrame, text='Tablets Price', font=('Times 14'), width=20)
priceLabel.grid(row=11, column=1)
price = Entry(stockFrame, width=43, textvariable=rate)
price.grid(row=11, column=2)
quantityLabel = Label(stockFrame, text='Product QT', font=('Times 14'), width=20)
quantityLabel.grid(row=12, column=1)
quantity = Entry(stockFrame, width=43, textvariable=qty)
quantity.grid(row=12, column=2)
rackLbl = Label(stockFrame, text='Rack#',font=('Times 14'), width=20)
rackLbl.grid(row=13, column=1)
rack = Entry(stockFrame, width=43, textvariable=rak)
rack.grid(row=13, column=2)

btnIns = Button(stockFrame, text='INSERT', font=('Times 14'), width=20, background='green', foreground='white', command=stock_insert)
btnIns.grid(row=15, column=1, padx=10, pady=10)
btnDel = Button(stockFrame, text='DELETE', font=('Times 14'), width=20, background='red', foreground='white', command=stock_delete)
btnDel.grid(row=15, column=2)
btnUpdate = Button(stockFrame, text='UPDATE', font=('Times 14'), width=20, background='blue', foreground='white', command=stock_update)
btnUpdate.grid(row=15, column=3, padx=10)

searchref = Label(stockFrame, text='Search By Medicine', font=('Times 14'), width=20)
searchref.grid(row=18, column=1, pady=30)
searchbx = ttk.Combobox(stockFrame, width=40, height=20, values=medlist)
searchbx.grid(row=18, column=2)
searchbx.set("Select One")
btnsearch = Button(stockFrame, text='SEARCH', font=('Times 14'), width=15, background='yellow', foreground='black', command=search_med)
btnsearch.grid(row=18, column=3)
btnreset = Button(stockFrame, text='RESET', font=('Times 14'), width=15, background='black', foreground='white', command=reset_table)
btnreset.grid(row=18, column=4, padx=10)

style = ttk.Style()
style.theme_use('clam')
scrollbarx = Scrollbar(stockFrame, orient=HORIZONTAL)
scrollbary = Scrollbar(stockFrame, orient=VERTICAL)

stocktable.configure(xscrollcommand=scrollbarx.set, yscrollcommand=scrollbary.set, selectmode='extended')
'''scrollbary.config(stocktable.yview())
scrollbarx.config(stocktable.xview())'''
scrollbarx.grid()
scrollbary.grid()
stocktable.column(1, anchor=CENTER, stretch=NO, width=70)
stocktable.heading(1, text='Referance#')
stocktable.column(2, anchor=CENTER, stretch=NO, width=100)
stocktable.heading(2, text='Company Name')
stocktable.column(3, anchor=CENTER, stretch=NO, width=100)
stocktable.heading(3, text='Medicine Name')
stocktable.column(4, anchor=CENTER, stretch=NO, width=100)
stocktable.heading(4, text='Type of Medicine')
stocktable.column(5, anchor=CENTER, stretch=NO, width=70)
stocktable.heading(5, text='Issue Date')
stocktable.column(6, anchor=CENTER, stretch=NO, width=70)
stocktable.heading(6, text='Expiry Date')
stocktable.column(7, anchor=CENTER, stretch=NO, width=100)
stocktable.heading(7, text='Uses')
stocktable.column(8, anchor=CENTER, stretch=NO, width=100)
stocktable.heading(8, text='Side effect')
stocktable.column(9, anchor=CENTER, stretch=NO, width=53)
stocktable.heading(9, text='Dosage')
stocktable.column(10, anchor=CENTER, stretch=NO, width=50)
stocktable.heading(10, text='Price')
stocktable.column(11, anchor=CENTER, stretch=NO, width=60)
stocktable.heading(11, text='Quantity')
stocktable.column(12, anchor=CENTER, stretch=NO, width=50)
stocktable.heading(12, text='Rack#')

stocktable.bind('<Double 1>', getrowstock)

# medicine profile
medRefLbl = Label(medFrame, text='Referance#', font=('Times 14'), width=20)
medRefLbl.grid(row=2, column=1, pady=20)
medRef = Entry(medFrame, width=40, textvariable=medreferance)
medRef.grid(row=2, column=2)
medNameLbl = Label(medFrame, text='Medicine Name', font=('Times 14'))
medNameLbl.grid(row=3, column=1)
medNameEnt = Entry(medFrame, width=40, textvariable=medicinename)
medNameEnt.grid(row=3, column=2)
medIns = Button(medFrame, text='INSERT', font=('Times 12'), background='green', foreground='white', command=med_insert)
medIns.grid(row=5, column=1)
medDel = Button(medFrame, text='DELETE', font=('Times 12'),background='red', foreground='white', command=med_delete)
medDel.grid(row=5, column=2)
medUpdate = Button(medFrame, text='UPDATE', font=('Times 12'), background='violet', foreground='white', command=med_update)
medUpdate.grid(row=5, column=3, pady=20)

# medicine list

medtable.grid(pady=10, padx=10, row=6, column=1, columnspan=3)
medtable.heading(1, text="Referance No")
medtable.heading(2, text="Medicine Name")
medtable.bind('<Double 1>', getrow)

bill = Button(medFrame, text='Generate Bill', font=('Times 14'), background='black', foreground='white', command=lambda: os.system('bill_generator.py'))
bill.grid(row=10, column=1, padx=20)

sales = Button(medFrame, text='Revenue Check', font=('Times 14'), background='black', foreground='white', command=lambda: os.system('sales.py'))
sales.grid(row=10, column=2, padx=20)
window.mainloop()