#!/usr/bin/env python3
from re import S
import tkinter as tk
from turtle import width
import pyodbc

username = 'teszt'
password = 'teszt'
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
'Server=DESKTOP-AQBCCTD;'
'UID=teszt;'
'PWD=teszt;'
'Database=techshop;'
'Trusted_Connection=yes;'
)
#Funkciók
def connecting():
    alert = tk.Tk()
    alert.geometry('250x150')
    username_text = tk.Label(alert, text="Username: ", font=("Arial", 12))
    username_text.grid(column=0, row=0)
    password_text = tk.Label(alert, text="Password: ", font=("Arial", 12))
    password_text.grid(column=0, row=1)
    username_entry = tk.Entry(alert)
    username_entry.grid(column=1, row=0)
    password_entry = tk.Entry(alert)
    password_entry.grid(column=1, row=1)
    alert.eval('tk::PlaceWindow . center')
    ok_button = tk.Button(alert, text="OK!", command=alert.destroy, width=10)
    ok_button.grid(columnspan=2, row=2)
    alert.mainloop()

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
    cursor.execute('Select name from ' + str(query))
    valamike = cursor.fetchall()
    if query == 'Product.products':
        label_select["text"] = 'Products'
    elif query == 'location.city':
        label_select["text"] = 'City'
    elif query == 'location.states':
        label_select["text"] = 'States'
    list(valamike)

def list(valami):
    lista.delete(0, tk.END)
    for item in valami:
        lista.insert(0, item[0].replace(',','').replace("'",'').replace('(','').replace(')',''))

def clear():
    lista.delete(0, tk.END)
    #Így kell meghívni egy másik scriptet.
    import another

def alert_box(alert_text):
    alert = tk.Tk()
    alert.geometry('250x150')
    alert_text = tk.Label(alert, text=alert_text, font=("Arial", 15))
    alert_text.pack()
    alert.eval('tk::PlaceWindow . center')
    ok_button = tk.Button(alert, text="OK!", command=alert.destroy, width=10)
    ok_button.pack()
    alert.mainloop()

def select():
    obj_name = lista.get(tk.ANCHOR).split(',')
    if not lista.get(tk.ANCHOR):
        alert_text="Product not selected!"
        alert_box(alert_text)
    else:
        print(obj_name[0])
        if label_select['text'] == 'Products':
            cursor = conn.cursor()
            cursor.execute("Select * from Product.products where name = '" + str(obj_name[0]) + "'")
            valamike = cursor.fetchall()
            more_info(obj_name, valamike)

def more_info(obj_name, input):
    stock = ''.join(str(e) for e in input)
    name_text = tk.Label(window, text="Name: ", font=("Arial", 12))
    name_text.grid(column=3, row=0)
    stock_text = tk.Label(window, text="Stock: ", font=("Arial", 12))
    stock_text.grid(column=3, row=1)
    name_entry = tk.Entry(window)
    name_entry.insert(tk.END, obj_name[0].replace('(','').replace(')',''))
    name_entry.grid(column=4, row=0)
    stock_entry = tk.Entry(window)
    stock_entry.insert(tk.END, stock.split(',')[4].replace(')',''))
    stock_entry.grid(column=4, row=1)

#Az ablak definiálása
window = tk.Tk()
window.title("DBStart Project")
window.geometry("800x600")
window.columnconfigure(0, minsize=100, pad=10)
window.columnconfigure(1, minsize=300)
window.columnconfigure(2, minsize=10)
window.columnconfigure(3, minsize=150)

label_select = tk.Label(text="Üdv!")
label_select.grid(column=1, row=0)

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

btn_connect = tk.Button(window, text="Connect", command=connecting, width=20)
btn_connect.grid(column=0, row=6, sticky=tk.NS)

list_scroll = tk.Scrollbar(window)
list_scroll.grid(column=2, row=1, rowspan=30, sticky=tk.N+tk.S)

lista = tk.Listbox(window, width=40, height=30, yscrollcommand = list_scroll.set)
lista.grid(column=1, row=1, sticky=tk.NE, rowspan=30)
list_scroll.config(command = lista.yview)

window.eval('tk::PlaceWindow . center')
window.mainloop()

def login():
    window = tk.Tk()
    label_select = tk.Label(text="Üdv!")
    label_select.grid(column=1, row=0)
    window.mainloop()
