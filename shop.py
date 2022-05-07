#!/usr/bin/env python3
import tkinter as tk
from turtle import width
import pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
'Server=DESKTOP-AQBCCTD;'
'UID=teszt;'
'PWD=teszt;'
'Database=techshop;'
'Trusted_Connection=yes;'
)

#Funkciók
def city():
    query = 'location.city'
    sql(query)

def state():
    query = 'location.states'
    sql(query)

def prod():
    query = 'Product.products'
    sql(query)

def sql(query):
    cursor = conn.cursor()
    cursor.execute('Select * from ' + str(query))
    valamike = cursor.fetchall()
    if query == 'Product.products':
        label_select["text"] = 'Products'
    elif query == 'location.city':
        label_select["text"] = 'City'
    elif query == 'location.states':
        label_select["text"] = 'States'
    list(valamike)

def list(valami):
    for item in valami:
        lista.insert(0, item)

def clear():
    lista.delete(0, tk.END)
    #Így kell meghívni egy másik scriptet.
    import another

def select():
    obj_name = lista.get(tk.ANCHOR).split(',')
    print(obj_name[1].rstrip(')'))
    if label_select['text'] == 'Products':
        cursor = conn.cursor()
        cursor.execute('Select * from Product.products where name = ' + str(obj_name[1]))
        valamike = cursor.fetchall()
        label_more["text"] = valamike

#Az ablak definiálása
window = tk.Tk()
window.title("DBStart Project")
window.geometry("800x600")
window.columnconfigure(0, minsize=100, pad=10)
window.columnconfigure(1, minsize=300)
window.columnconfigure(2, minsize=150)

label_select = tk.Label(text="Üdv!")
label_select.grid(column=1, row=0)

label_more = tk.Label(text="Üdv!")
label_more.grid(column=2, row=0)

label = tk.Label(text="DBStart Python")
label.grid(column=0, row=0, sticky=tk.NS)

#Gomb, mérettel és pozícióval
btn_state = tk.Button(window, text="States", command=state, width=20)
btn_state.grid(column=0, row=1, sticky=tk.NS)

btn_city = tk.Button(window, text="City", command=city, width=20)
btn_city.grid(column=0, row=2, sticky=tk.NS)
#btn_city.place(x=15, y=15, width=100, height=40)
btn_Prod = tk.Button(window, text="Products", command=prod, width=20)
btn_Prod.grid(column=0, row=3, sticky=tk.NS)

btn_clear = tk.Button(window, text="Clear", command=clear, width=20)
btn_clear.grid(column=0, row=4, sticky=tk.NS)

btn_select = tk.Button(window, text="Select", command=select, width=20)
btn_select.grid(column=0, row=5, sticky=tk.NS)

lista = tk.Listbox(window, width=40, height=30)
lista.grid(column=1, row=1, sticky=tk.NS, rowspan=30)

window.mainloop()