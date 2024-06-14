import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3


try:
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    print("Database connected successfully")
except sqlite3.Error as e:
    print(f"Database connection error: {e}")
    exit()


try:
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    print("Table created successfully")
except sqlite3.Error as e:
    print(f"Table creation error: {e}")


def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    print(f"Adding contact: Name={name}, Phone={phone}")  # Debugging output
    if name and phone:
        try:
            c.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
            conn.commit()
            entry_name.delete(0, tk.END)
            entry_phone.delete(0, tk.END)
            messagebox.showinfo("Success", "Contact added successfully")
            show_contacts()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to add contact: {e}")
    else:
        messagebox.showerror("Error", "Please enter both name and phone")


def show_contacts():
    for row in tree.get_children():
        tree.delete(row)
    try:
        c.execute('SELECT * FROM contacts')
        for row in c.fetchall():
            print(f"Fetched row: {row}")  # Debugging output
            tree.insert('', tk.END, values=row)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to retrieve contacts: {e}")


def delete_contact():
    selected_item = tree.selection()[0]
    contact_id = tree.item(selected_item)['values'][0]
    print(f"Deleting contact with ID={contact_id}")  # Debugging output
    try:
        c.execute('DELETE FROM contacts WHERE id=?', (contact_id,))
        conn.commit()
        tree.delete(selected_item)
        messagebox.showinfo("Success", "Contact deleted successfully")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to delete contact: {e}")


def update_contact():
    selected_item = tree.selection()[0]
    contact_id = tree.item(selected_item)['values'][0]
    new_name = entry_name.get()
    new_phone = entry_phone.get()
    print(f"Updating contact ID={contact_id} to Name={new_name}, Phone={new_phone}")  # Debugging output
    if new_name and new_phone:
        try:
            c.execute('UPDATE contacts SET name=?, phone=? WHERE id=?', (new_name, new_phone, contact_id))
            conn.commit()
            entry_name.delete(0, tk.END)
            entry_phone.delete(0, tk.END)
            messagebox.showinfo("Success", "Contact updated successfully")
            show_contacts()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to update contact: {e}")
    else:
        messagebox.showerror("Error", "Please enter both name and phone")


root = tk.Tk()
root.title("Contact Manager")

frame = tk.Frame(root)
frame.pack(pady=20)

label_name = tk.Label(frame, text="Name")
label_name.grid(row=0, column=0)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1)

label_phone = tk.Label(frame, text="Phone")
label_phone.grid(row=1, column=0)
entry_phone = tk.Entry(frame)
entry_phone.grid(row=1, column=1)

button_add = tk.Button(frame, text="Add Contact", command=add_contact)
button_add.grid(row=2, column=0, columnspan=2, pady=10)

columns = ('id', 'name', 'phone')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('id', text='ID')
tree.heading('name', text='Name')
tree.heading('phone', text='Phone')
tree.pack(pady=20)

button_update = tk.Button(root, text="Update Contact", command=update_contact)
button_update.pack(pady=5)
button_delete = tk.Button(root, text="Delete Contact", command=delete_contact)
button_delete.pack(pady=5)

show_contacts()

root.mainloop()

# Fermer la connexion à la base de données
conn.close()
