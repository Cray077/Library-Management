from tkinter import *
from tkinter import ttk
from datetime import datetime
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

def update_book(book, edit, value):
    if edit == "title":
        with conn:
            cur.execute("UPDATE books SET title = :value WHERE title= :title AND id_num=id_num", 
                    {"value": value, "title": book[0], "id_num": book[4]})
    elif edit == "author":
        with conn:
            cur.execute("UPDATE books SET author = :value WHERE title= :title AND id_num=id_num", 
                    {"value": value, "title": book[0], "id_num": book[4]})
    elif edit == "year":
        with conn:
            cur.execute("UPDATE books SET year = :value WHERE title= :title AND id_num=id_num", 
                    {"value": value, "title": book[0], "id_num": book[4]})
    elif edit == "isbn":
        with conn:
            cur.execute("UPDATE books SET isbn = :value WHERE title= :title AND id_num=id_num", 
                    {"value": value, "title": book[0], "id_num": book[4]})
    elif edit == "id num":
        with conn:
            cur.execute("UPDATE books SET id_num = :value WHERE title= :title AND id_num=id_num", 
                    {"value": value, "title": book[0], "id_num": book[4]})
    elif edit == "desc":
        with conn:
            cur.execute("UPDATE books SET descript = :value WHERE title= :title AND id_num=id_num", 
                    {"value": value, "title": book[0], "id_num": book[4]})
    
    else: print("Error Unknown Value!!!!")

def delete_book(book):
    with conn:
        cur.execute("DELETE FROM books WHERE title= :title AND id_num= :id_num",
                {"title": book[0], "id_num": book[4]})

def search_database(key, value):
    pass

def sort_database():
    pass

# Create Table in SQL
try:
    create_table()
except sqlite3.OperationalError:
    print("Okay")


####################################################################################################
#SEPARATOR                                                                                         
####################################################################################################
# Main GUI
root = Tk()

root.title("Library Book's Management")

# Frame

entry = LabelFrame(root, padx=10, pady=10)
treeview = LabelFrame(root, padx=10, pady=10)

# Treeview
tree = ttk.Treeview(treeview)

# Define Columns
tree["columns"] = ("Title", "Author", "Year", "Isbn", "ID", "Time", "Description")

tree.column("#0", width=35, anchor=W)
tree.column("Title", width=120, anchor=W)
tree.column("Author", width=120, anchor=W)
tree.column("Year", width=120, anchor=W)
tree.column("Isbn", width=120, anchor=W)
tree.column("ID", width=120)
tree.column("Time", width=120, anchor=W)
tree.column("Description", width=120, anchor=W)

# Define Headings
tree.heading("#0", text = "Num", anchor=W)
tree.heading("Title", text ="Title", anchor=W)
tree.heading("Author", text = "Author", anchor=W)
tree.heading("Year", text = "Year", anchor=W)
tree.heading("Isbn", text = "ISBN", anchor=W)
tree.heading("ID", text = "ID")
tree.heading("Time", text = "Time", anchor=W)
tree.heading("Description",text = "Description", anchor=W)

# Insert Data to Treeview
database = read_database()
for x in database:
    num = (database.index(x) + 1)
    tree.insert(parent= "", index= "end", iid= num, text= num,values = (x[0],x[1],x[2],x[3],x[4],x[5],x[6]))


# Entry
title = Entry(entry, width=40)
author = Entry(entry, width=40)
year = Entry(entry, width=40)
isbn = Entry(entry, width=40)
id_num = Entry(entry, width=40)
descript = Entry(entry, width=40)

#Label

title_lb = Label(entry, text="Title")
author_lb = Label(entry, text="Author")
year_lb = Label(entry, text="Year")
isbn_lb = Label(entry, text="ISBN")
id_lb = Label(entry, text="ID")
desc_lb = Label(entry, text="Description")


# Functions
def save():
    data1 = title.get()
    data2 = author.get()
    data3 = year.get()
    data4 = isbn.get()
    data5 = id_num.get()
    data6 = datetime.today()
    data7 = descript.get()

    data = (data1,data2,data3,data4,data5, data6, data7)
    add_book(data)
    database = read_database()
    num = (len(database))

    tree.insert(parent= "", index= "end", iid= num, text= num,values = (data1, data2, data3, data4, data5, data6, data7))


def read():
    data = read_database()
    num = 1
    for x in data:
        print(num, x)
        num += 1


# Buttons
btn_save = Button(entry, text="Save", command = save, width=15)
btn_read = Button(entry, text="Read", command = read, width=15)


# Grid
entry.grid(row=0, column=1)
treeview.grid(row=0, column=0)

tree.grid(row=0, column= 0)

title.grid(row = 1, column = 0, columnspan = 3)
author.grid(row = 3, column = 0, columnspan = 3)
year.grid(row = 5, column = 0, columnspan = 3)
isbn.grid(row = 7, column = 0, columnspan = 3)
id_num.grid(row = 9, column = 0, columnspan = 3)
descript.grid(row = 11, column = 0, columnspan = 3)


btn_save.grid(row = 12, column = 1)
btn_read.grid(row = 13, column = 1)

title_lb.grid(row = 0, column = 0) 
author_lb.grid(row = 2, column = 0) 
year_lb.grid(row = 4, column = 0) 
isbn_lb.grid(row = 6, column = 0) 
id_lb.grid(row = 8, column = 0) 
desc_lb.grid(row = 10, column = 0)  

root.mainloop()
conn.close()
