from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
import sqlite3


root = Tk()
root.title("Address Database")
root.geometry("400x400")


#Databases
conn = sqlite3.connect('address_book.db')

#Create cursor
c = conn.cursor()

#Create table
'''
c.execute("""CREATE TABLE addresses (
		first_name text, 
		last_name text,
		address text,
		city text,
		state text,
		zipcode integer
		)""")
'''


#Create update fn for editted record
def update():
	#Databases
	conn = sqlite3.connect('address_book.db')
	#Create cursor
	c = conn.cursor()

	record_id = delete_box.get()
	c.execute("""UPDATE addresses SET
		first_name = :first, 
		last_name = :last,
		address = :address,
		city = :city,
		state = :state,
		zipcode = :zipcode\

		WHERE oid = :oid""",
		{
		'first' : f_name_editor.get(),
		'last' : l_name_editor.get(),
		'address' : address_editor.get(),
		'city' : city_editor.get(),
		'state' : state_editor.get(),
		'zipcode' : zipcode_editor.get(),

		'oid' : record_id
		})


	#commit changes
	conn.commit()
	#Close connection
	conn.close()

	editor.destroy()


#Create an edit fn
def edit():
	global editor
	editor = Tk()
	editor.title("Update a record")
	editor.geometry("400x400")

	#Databases
	conn = sqlite3.connect('address_book.db')
	#Create cursor
	c = conn.cursor()

	record_id = delete_box.get()
	#Query the database
	c.execute("SELECT * FROM addresses WHERE oid = " + record_id)
	records = c.fetchall()

	#Create global variablea
	global f_name_editor
	global l_name_editor
	global address_editor
	global city_editor
	global state_editor
	global zipcode_editor

	#Create text boxes
	f_name_editor = Entry(editor, width=30)
	f_name_editor.grid(row=0, column=1, padx=20, pady = (10, 0))
	l_name_editor = Entry(editor, width=30)
	l_name_editor.grid(row=1, column=1)
	address_editor = Entry(editor, width=30)
	address_editor.grid(row=2, column=1)
	city_editor = Entry(editor, width=30)
	city_editor.grid(row=3, column=1)
	state_editor = Entry(editor, width=30)
	state_editor.grid(row=4, column=1)
	zipcode_editor = Entry(editor, width=30)
	zipcode_editor.grid(row=5, column=1)
	
	#Create text box labels
	f_name_label = Label(editor, text="First Name").grid(row=0, column=0, pady = (10, 0))
	l_name_label = Label(editor, text="Last Name").grid(row=1, column=0)
	address_label = Label(editor, text="Address").grid(row=2, column=0)
	city_label = Label(editor, text="City").grid(row=3, column=0)
	state_label = Label(editor, text="State").grid(row=4, column=0)
	zipcode_label = Label(editor, text="Zipcode").grid(row=5,column=0)

	#Loop through results
	for record in records:
		f_name_editor.insert(0, record[0])
		l_name_editor.insert(0, record[1])
		address_editor.insert(0, record[2])
		city_editor.insert(0, record[3])
		state_editor.insert(0, record[4])
		zipcode_editor.insert(0, record[5])

 	#Create a save button to save editted
	edit_btn = Button(editor, text="Save  Record", command=update)
	edit_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=141)

#Create a fn to delete record
def delete():
	#Databases
	conn = sqlite3.connect('address_book.db')
	#Create cursor
	c = conn.cursor()

	#delete a record
	c.execute("DELETE from addresses WHERE oid=" + delete_box.get())

	#commit changes
	conn.commit()
	#Close connection
	conn.close()	


#create submit fn
def submit():
	#Databases
	conn = sqlite3.connect('address_book.db')
	#Create cursor
	c = conn.cursor()

	#Insert into table
	c.execute("INSERT INTO addresses VALUES(:f_name, :l_name, :address, :city, :state, :zipcode)",
			{
				'f_name' : f_name.get(),
				'l_name' : l_name.get(),
				'address' : address.get(),
				'city' : city.get(),
				'state' : state.get(),
				'zipcode' : zipcode.get()
			})

	#commit changes
	conn.commit()
	#Close connection
	conn.close()


	#clear the text boxes
	f_name.delete(0, END)
	l_name.delete(0, END)
	address.delete(0, END)
	city.delete(0, END)
	state.delete(0, END)
	zipcode.delete(0, END)


#Create query function
def query():
	#Databases
	conn = sqlite3.connect('address_book.db')
	#Create cursor
	c = conn.cursor()
	#Query th3e database
	c.execute("SELECT *, oid FROM addresses")
	records = c.fetchall()

	#Loop through results
	print_records = ''
	for record in records:
		print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[6]) + "\n"

	query_label = Label(root, text=print_records)
	query_label.grid(row=11, column=0, columnspan=2)

	#commit changes
	conn.commit()
	
	 #Close connection
	conn.close()


#Create text boxes
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady = (10, 0))
l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)
address = Entry(root, width=30)
address.grid(row=2, column=1)
city = Entry(root, width=30)
city.grid(row=3, column=1)
state = Entry(root, width=30)
state.grid(row=4, column=1)
zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1)

delete_box = Entry(root, width = 30)
delete_box.grid(row=9, column=1)


#Create text box labels
f_name_label = Label(root, text="First Name").grid(row=0, column=0, pady = (10, 0))
l_name_label = Label(root, text="Last Name").grid(row=1, column=0)
address_label = Label(root, text="Address").grid(row=2, column=0)
city_label = Label(root, text="City").grid(row=3, column=0)
state_label = Label(root, text="State").grid(row=4, column=0)
zipcode_label = Label(root, text="Zip Code").grid(row=5, column=0)
delete_box_label = Label(root, text ="Select ID").grid(row=9, column=0)

#Create submit byutton
submit_btn = Button(root, text="Add record to database", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=10) 


#Create a query button
query_btn = Button(root, text="Show Record", command=query)
query_btn.grid(row=7, column=0, columnspan=2, padx=10, pady=10, ipadx=137)


#Create a delete buttom
delete_btn = Button(root, text="Delete  Record", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, padx=10, pady=10, ipadx=134)


#Create an update button 
edit_btn = Button(root, text="Edit  Record", command=edit)
edit_btn.grid(row=12, column=0, columnspan=2, padx=10, pady=10, ipadx=141)


#commit changes
conn.commit()

#Close connection
conn.close()


mainloop()