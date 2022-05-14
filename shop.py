#!/usr/bin/env python3
from re import S
from sre_constants import SUCCESS
import tkinter as tk
from turtle import width
import pyodbc
#Másik script meghívása
import another
server = 'localhost'
username = ''
password = ''
clear = '0'
#Funkciók
def connection():
    global server
    global username
    global password
    global conn
    try:
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
        'Server=' +str(server) + ";"
        #'Server=DESKTOP-AQBCCTD;'
        'UID=' +str(username) + ";"
        'PWD=' +str(password) + ";"
        'Database=techshop;'
        'Trusted_Connection=no;')
        connect_success()
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '28000':
            connect_failed()

def connecting():
    global alert
    alert = tk.Tk()
    alert.geometry('250x150')
    global username
    global password
    global server
    global username_entry
    global password_entry
    global server_entry
    username_text = tk.Label(alert, text="Username: ", font=("Arial", 12))
    username_text.grid(column=0, row=0)
    password_text = tk.Label(alert, text="Password: ", font=("Arial", 12))
    password_text.grid(column=0, row=1)
    server_text = tk.Label(alert, text="Server name: ", font=("Arial", 12))
    server_text.grid(column=0, row=2)
    username_entry = tk.Entry(alert)
    username_entry.insert(tk.END, username)
    username_entry.grid(column=1, row=0)
    password_entry = tk.Entry(alert, show="*")
    password_entry.insert(tk.END, password)
    password_entry.grid(column=1, row=1)
    server_entry = tk.Entry(alert)
    server_entry.insert(tk.END, server)
    server_entry.grid(column=1, row=2)
    ok_button = tk.Button(alert, text="OK!", command=check_connect, width=10)
    ok_button.grid(columnspan=2, row=3)
    alert.eval('tk::PlaceWindow . center')
    alert.mainloop()

def check_connect():
    global username
    global password
    global username_entry
    global password_entry
    username = username_entry.get()
    password = password_entry.get()
    connection()

def connect_success():
    global success_screen
    success_screen = tk.Tk()
    success_screen.geometry('250x150')
    success_label = tk.Label(success_screen, text='Login Successful!', font=("Arial", 12))
    success_label.pack()
    success_button = tk.Button(success_screen, text='OK!', command=del_screen)
    success_button.pack()
    success_screen.eval('tk::PlaceWindow . center')

def connect_failed():
    global connect_fail
    connect_fail = tk.Tk()
    connect_fail.geometry('250x150')
    fail_label = tk.Label(connect_fail, text='Login Failed!', font=("Arial", 12))
    fail_label.pack()
    fail_button = tk.Button(connect_fail, text='OK!', command=del_fail)
    fail_button.pack()
    connect_fail.eval('tk::PlaceWindow . center')

def del_fail():
    global connect_fail
    connect_fail.destroy()

def del_screen():
    global success_screen
    global alert
    success_screen.destroy()
    alert.destroy()

def city():
    query = 'location.city'
    sql(query)

def state():
    query = 'location.states'
    sql(query)

def prod():
    query = 'Product.products'
    sql(query)

def orders():
    query = 'Orders.orders'
    cursor = conn.cursor()
    cursor.execute('Select id from ' + str(query))
    order_fetch = cursor.fetchall()
    label_select["text"] = 'Orders'
    list(order_fetch)

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
    if label_select["text"] == 'Orders':
        for item in valami:
            lista.insert(0, item[0])
    else:
        for item in valami:
            lista.insert(0, item[0].replace(',','').replace("'",'').replace('(','').replace(')',''))

def clear():
    lista.delete(0, tk.END)
    another.teszt()

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
        alert_text="Nothing selected!"
        alert_box(alert_text)
    else:
        print(obj_name[0])
        if label_select['text'] == 'Products':
            cursor = conn.cursor()
            cursor.execute("Select * from Product.products p left join product.categories c on c.id = p.category_id where p.name = '" + str(obj_name[0]) +"'")
            fetch = cursor.fetchall()
            more_info(obj_name, fetch)
        elif label_select['text'] == 'City':
            cursor = conn.cursor()
            cursor.execute("Select * from location.city where name = '" + str(obj_name[0]) +"'")
            fetch = cursor.fetchall()
            more_info(obj_name, fetch)
        elif label_select['text'] == 'States':
            cursor = conn.cursor()
            cursor.execute("Select * from location.states where name = '" + str(obj_name[0]) +"'")
            fetch = cursor.fetchall()
            more_info(obj_name, fetch)

def more_info(obj_name, input):
    if label_select['text'] == 'Products':
        stock = ''.join(str(e) for e in input)
        global prod_id
        #ID
        prod_id = stock.split(',')[0].replace('(','')
        global name_entry
        global stock_entry
        global category_entry
        global price_entry
        name_entry.delete(0, tk.END)
        name_entry.insert(tk.END, obj_name[0].replace('(','').replace(')',''))
        stock_entry.delete(0, tk.END)
        stock_entry.insert(tk.END, stock.split(',')[4].replace(')',''))
        category_entry.delete(0, tk.END)
        category_entry.insert(tk.END, stock.split(',')[6].replace(')','').replace("'",''))
        price_entry.delete(0, tk.END)
        price_entry.insert(tk.END, stock.split(',')[3].replace(')',''))
    elif label_select['text'] == 'City':
        if frame in globals():
            frame.destroy()
        elif stateframe in globals():
            stateframe.destroy()
        cityframe = tk.Frame()
        cityframe.grid(column=3, columnspan=3, row=0, rowspan=30, sticky=tk.N)
        text_label = tk.Label(cityframe, text="City info")
        text_label.grid(column=3, columnspan=2, row=0)
        name_text = tk.Label(cityframe, text="Name: ", font=("Arial", 12))
        name_text.grid(column=3, row=1, sticky=tk.W)
        stock_text = tk.Label(cityframe, text="ID: ", font=("Arial", 12))
        stock_text.grid(column=3, row=2, sticky=tk.W)
        name_entry = tk.Entry(cityframe)
        name_entry.grid(column=4, row=1)
        stock_entry = tk.Entry(cityframe)
        stock_entry.grid(column=4, row=2)
    elif label_select['text'] == 'States':
        if cityframe in globals():
            cityframe.destroy()
        elif frame in globals():
            frame.destroy()
        stateframe = tk.Frame()
        stateframe.grid(column=3, columnspan=3, row=0, rowspan=30, sticky=tk.N)
        text_label = tk.Label(stateframe, text="States info")
        text_label.grid(column=3, columnspan=2, row=0)
        name_text = tk.Label(stateframe, text="Name: ", font=("Arial", 12))
        name_text.grid(column=3, row=1, sticky=tk.W)
        stock_text = tk.Label(stateframe, text="ID: ", font=("Arial", 12))
        stock_text.grid(column=3, row=2, sticky=tk.W)
        name_entry = tk.Entry(stateframe)
        name_entry.grid(column=4, row=1)
        stock_entry = tk.Entry(stateframe)
        stock_entry.grid(column=4, row=2)

def modify():
    prod_name = name_entry.get()
    prod_stock = stock_entry.get()
    prod_category = category_entry.get()
    prod_price = price_entry.get()
    print(prod_name, prod_stock, prod_category, prod_price)
    cursor = conn.cursor()
    cursor.execute("UPDATE Product.products SET name = '" + str(prod_name) \
        +"', stock = '" + str(prod_stock) + "', price = '" + str(prod_price) \
            +"' where id = '" + str(prod_id) +"'")
    commit = cursor.commit()
    print(commit)

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
btn_Prod = tk.Button(window, text="Products", command=prod, width=20)
btn_Prod.grid(column=0, row=3, sticky=tk.NS)
btn_clear = tk.Button(window, text="Clear", command=clear, width=20)
btn_clear.grid(column=0, row=4, sticky=tk.NS)
btn_select = tk.Button(window, text="Select", command=select, width=20)
btn_select.grid(column=0, row=5, sticky=tk.NS)
btn_connect = tk.Button(window, text="Connect", command=connecting, width=20)
btn_connect.grid(column=0, row=6, sticky=tk.NS)
btn_orders = tk.Button(window, text="Orders", command=orders, width=20)
btn_orders.grid(column=0, row=7, sticky=tk.NS)
list_scroll = tk.Scrollbar(window)
list_scroll.grid(column=2, row=1, rowspan=30, sticky=tk.N+tk.S)

#Info frame
frame = tk.Frame(window)
frame.grid(column=3, columnspan=3, row=0, rowspan=30, sticky=tk.N)
text_label = tk.Label(frame, text="Product info")
text_label.grid(column=3, columnspan=2, row=0)
name_text = tk.Label(frame, text="Name: ", font=("Arial", 12))
name_text.grid(column=3, row=1, sticky=tk.W)
stock_text = tk.Label(frame, text="Stock: ", font=("Arial", 12))
stock_text.grid(column=3, row=2, sticky=tk.W)
category_text = tk.Label(frame, text="Category: ", font=("Arial", 12))
category_text.grid(column=3, row=3, sticky=tk.W)
price_text = tk.Label(frame, text="Price: ", font=("Arial", 12))
price_text.grid(column=3, row=4, sticky=tk.W)
name_entry = tk.Entry(frame)
name_entry.grid(column=4, row=1)
stock_entry = tk.Entry(frame)
stock_entry.grid(column=4, row=2)
category_entry = tk.Entry(frame)
category_entry.grid(column=4, row=3)
price_entry = tk.Entry(frame)
price_entry.grid(column=4, row=4)
btn_modify = tk.Button(frame, text="Modify data", command=modify)
btn_modify.grid(column=3, columnspan=2, row=8)
#Lista
lista = tk.Listbox(window, width=40, height=30, yscrollcommand = list_scroll.set)
lista.grid(column=1, row=1, sticky=tk.NE, rowspan=30)
list_scroll.config(command = lista.yview)

window.eval('tk::PlaceWindow . center')
connecting()
window.mainloop()
