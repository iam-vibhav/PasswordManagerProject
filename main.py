import tkinter as tk
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    small_letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
    capital_letters = [chr(i) for i in range(ord('A'), ord('Z')+1)]
    numbers = [chr(i) for i in range(ord('0'), ord('9')+1)]
    special_symbols = ['!', '@', '#', '$', '%', '^', '&', '*']

    n_small = random.randint(2, 5)
    n_capital = random.randint(2, 5)
    n_numbers = random.randint(2, 5)
    n_symbols = random.randint(2, 5)

    password_list = []

    for i in range(n_small):
        password_list.append(random.choice(small_letters))
    for i in range(n_capital):
        password_list.append(random.choice(capital_letters))
    for i in range(n_numbers):
        password_list.append(random.choice(numbers))
    for i in range(n_symbols):
        password_list.append(random.choice(special_symbols))
    random.shuffle(password_list)
    password_string = "".join(password_list)
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password_string)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if website == "" or username == "" or password == "":
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty")
    else:
        confirmation_string = f"Are you sure you want to add the following details?\nUsername/Email: {username}\nPassword: {password}"
        is_ok = messagebox.askokcancel(title=website, message=confirmation_string)
        if is_ok:
            new_entry = {website: {'email': username, 'password': password}}
            try:
                with open("password.json", "r") as password_file:
                    try:
                        data = json.load(password_file)
                    except json.JSONDecodeError:
                        data = {}
                    data.update(new_entry)
                with open("password.json", "w") as password_file:
                    json.dump(data, password_file, indent=4)
            except FileNotFoundError:
                with open("password.json", "w") as password_file:
                    json.dump(new_entry, password_file, indent=4)

            website_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            try:
                pyperclip.copy(password)
            except pyperclip.PyperclipException:
                messagebox.showwarning(title="Error", message="Failed to copy password to clipboard")


# ---------------------------- WEBSITE SEARCHER ------------------------------- #


def search():
    website = website_entry.get()
    try:
        with open("password.json", "r") as password_file:
            data = json.load(password_file)
            if website in data:
                username = data[website]['email']
                password = data[website]['password']
                messagebox.showinfo(title=website, message=f"Username/Email: {username}\nPassword: {password}")
            else:
                messagebox.showinfo(title="Oops", message="You didn't save this website's details")
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="You didn't save this website's details")
    except json.JSONDecodeError:
        messagebox.showinfo(title="Oops", message="You didn't save this website's details")



# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = tk.Canvas(width=200, height=200)
logo = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

website_label = tk.Label(text="Website:")
website_label.grid(row=1, column=0)
username_label = tk.Label(text="Username / Email:")
username_label.grid(row=2, column=0)
password_label = tk.Label(text="Password:")
password_label.grid(row=3, column=0)

website_entry = tk.Entry(width=31)
website_entry.grid(row=1, column=1, columnspan=1)
website_entry.focus()
username_entry = tk.Entry(width=50)
username_entry.grid(row=2, column=1, columnspan=2)
password_entry = tk.Entry(width=31)
password_entry.grid(row=3, column=1)

generate_password_button = tk.Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = tk.Button(text="Add", width=45, command=add_password)
add_button.grid(row=4, column=1, columnspan=2)
search_button = tk.Button(text="Search", command=search)
search_button.config(width=15)
search_button.grid(row=1, column=2)

window.mainloop()
