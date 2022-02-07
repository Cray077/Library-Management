from tkinter import *
from tkinter import ttk
from datetime import date
import sqlite3

# SQL Variables
conn = sqlite3.Connection("database.db")
cur = conn.cursor()

# SQL Functions

def create_table():
    with conn:
        cur.execute("""CREATE TABLE books (
                title text PRIMARY KEY,
                author text,
                year text,
                isbn text,
                id_num text,
                datetime text,
                descript text)""")

def drop_table():
    with conn:
        cur.execute("DROP TABLE books")


def add_book(book):
    with conn:
        cur.execute("INSERT INTO books VALUES (:title, :author, :year, :isbn, :id_num, :datetime, :descript)", 
                {"title": book[0], "author": book[1], "year": book[2], "isbn": book[3], "id_num": book[4], "datetime": book[5], "descript": book[6]})

def read_database():
    cur.execute("SELECT * FROM books")
    return cur.fetchall()


def delete_book(book):
    with conn:
        cur.execute("DELETE FROM books WHERE title= :title AND id_num= :id_num",
                {"title": book[0], "id_num": book[4]})

# Create Table in SQL
try:
    create_table()
except sqlite3.OperationalError:
    print("Okay")


######################################### SEPARATOR ###########################################################
# Main GUI
root = Tk()
root.title("Library Book's Management")

# Frame
entry = LabelFrame(root, padx=10, pady=10)
treeview = LabelFrame(root)

# Treeview
tree = ttk.Treeview(treeview)

# Define Columns
tree["columns"] = ("Title", "Author", "Year", "Isbn", "ID", "Time", "Description")

tree.column("#0", width=35, stretch=False, anchor=W)
tree.column("Title", width=90, stretch=False, anchor=W)
tree.column("Author", width=20, stretch=False, anchor=W)
tree.column("Year", width=50, stretch=False, anchor=W)
tree.column("Isbn", width=70, stretch=False, anchor=W)
tree.column("ID", width=70, stretch=False)
tree.column("Time", width=20, stretch=False, anchor=W)
tree.column("Description", width=120, stretch=False, anchor=W)

# Define Headings
tree.heading("#0", text = "Num", anchor=W)
tree.heading("Title", text ="Title", anchor=W)
tree.heading("Author", text = "Author", anchor=W)
tree.heading("Year", text = "Year", anchor=W)
tree.heading("Isbn", text = "ISBN", anchor=W)
tree.heading("ID", text = "ID")
tree.heading("Time", text = "Time", anchor=W)
tree.heading("Description",text = "Description", anchor=W)

######################## Scrollbar ###############################
# Scrollbar Vertical
scrollbar = ttk.Scrollbar(treeview, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)

# Scrollbar Horizontal
scrollbar_hor = ttk.Scrollbar(treeview, orient="horizontal", command=tree.xview)
tree.configure(xscroll=scrollbar_hor.set)

# Insert Data to Treeview
def insert_data():
    database = read_database()
    num = 1
    for x in database:
        tree.insert(parent= "", index= "end", iid= num, text= num,values = (x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
        num += 1
insert_data()

def remove_data():
    for x in tree.get_children():
        tree.delete(x)

# Entry
title = Entry(entry, width=30)
author = Entry(entry, width=30)
year = Entry(entry, width=30)
isbn = Entry(entry, width=30)
id_num = Entry(entry, width=30)
descript = Entry(entry, width=30)

search_bar = Entry(treeview, width= 50)

#Label

title_lb = Label(entry, text="Title", anchor="w")
author_lb = Label(entry, text="Author", anchor="w")
year_lb = Label(entry, text="Year", anchor="w")
isbn_lb = Label(entry, text="ISBN", anchor="w")
id_lb = Label(entry, text="ID", anchor="w")
desc_lb = Label(entry, text="Description", anchor="w")


# Functions
def clear_entry():
    title.delete(0, END)
    author.delete(0, END)
    year.delete(0,END)
    isbn.delete(0,END)
    id_num.delete(0, END)
    descript.delete(0, END)

def save():
    data1 = title.get()
    data2 = author.get()
    data3 = year.get()
    data4 = isbn.get()
    data5 = id_num.get()
    data6 = date.today()
    data7 = descript.get()

    data = (data1,data2,data3,data4,data5, data6, data7)
    add_book(data)
    database = read_database()
    num = (len(database))
    clear_entry()

    tree.insert(parent= "", index= "end", iid= num, text= num,values = (data1, data2, data3, data4, data5, data6, data7))


def read():
    data = read_database()
    num = 1
    for x in data:
        print(num, x)
        num += 1

def edit():
    select = tree.focus()
    data = tree.item(select, "values")

    print(data)
    title.insert(0, data[0])
    author.insert(0, data[1])
    year.insert(0, data[2])
    isbn.insert(0, data[3])
    id_num.insert(0, data[4])
    descript.insert(0, data[6])

def update():
    select = tree.focus()
    tree.item(select, values=(
   
    title.get(),
    author.get(),
    year.get(),
    isbn.get(),
    id_num.get(),
    date.today(),
    descript.get()
    ))
    with conn:

        cur.execute("UPDATE books SET title=:title, author=:author,year=:year,isbn=:isbn, id_num= :id_num,datetime= :datetime,descript=:descript WHERE title= :title AND id_num=id_num", 
                {   "title": title.get(),
                    "author": author.get(),
                    "year": year.get(),
                    "isbn": isbn.get(),
                    "id_num": id_num.get(),
                    "datetime": date.today(),
                    "descript": descript.get()
                    })


    clear_entry()


def delete():
    select = tree.selection()
    for x in select:
        book = tree.item(x, "values")
        delete_book(book)
        tree.delete(x)

def search():
    key = "author"
    value = search_bar.get()
    data = read_database()
    ls = ("title", "author", "year", "isbn", "id_num", "datetime", "descript")
    found = []
    for x in data:
        if value.lower() in x[ls.index(key)].lower():
            found.append(x)
    remove_data()
    num = 1
    for x in found:
        tree.insert(parent= "", index= "end", iid= num, text= num,values = (x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
        num += 1



# Buttons
btn_save = Button(entry, text="Save", command = save, width=10)
btn_read = Button(entry, text="Read", command = read, width=10)
btn_edit = Button(entry, text="Edit", command = edit, width=10)
btn_delete = Button(entry, text="Delete", command = delete, width=10)
btn_update = Button(entry, text="Update", command = update, width=10)
btn_search = Button(treeview, text="Search", command=search, width=10)


# Grid
entry.grid(row=0, column=1)
treeview.grid(row=0, column=0)

btn_search.grid(row=0, column=1)
search_bar.grid(row=0, column=0)
tree.grid(row=1, column= 0, columnspan=2)

scrollbar.grid(row=1, column=2, sticky="ns")
scrollbar_hor.grid(row=2, column=0, sticky="ew", columnspan=2)

title.grid(row = 1, column = 0, columnspan = 3)
author.grid(row = 3, column = 0, columnspan = 3)
year.grid(row = 5, column = 0, columnspan = 3)
isbn.grid(row = 7, column = 0, columnspan = 3)
id_num.grid(row = 9, column = 0, columnspan = 3)
descript.grid(row = 11, column = 0, columnspan = 3)

btn_save.grid(row = 12, column = 0)
btn_read.grid(row = 13, column = 0)
btn_edit.grid(row = 12, column = 1)
btn_delete.grid(row = 13, column = 1)
btn_update.grid(row = 12, column = 2)

title_lb.grid(row = 0, column = 0) 
author_lb.grid(row = 2, column = 0) 
year_lb.grid(row = 4, column = 0) 
isbn_lb.grid(row = 6, column = 0) 
id_lb.grid(row = 8, column = 0) 
desc_lb.grid(row = 10, column = 0)  



root.mainloop()
conn.close()
