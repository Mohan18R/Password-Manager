import json
from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            email_entry.delete(0,END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Creating a frame to group widgets
frame = Frame(window, padx=20, pady=20)
frame.grid(row=1, column=1)

canvas = Canvas(frame, width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=0, columnspan=3)

website_label = Label(frame, text="Website:")
website_label.grid(row=1, column=0, pady=(10, 0), sticky="e")

email_label = Label(frame, text="Email/Username:")
email_label.grid(row=2, column=0, pady=(10, 0), sticky="e")

password_label = Label(frame, text="Password:")
password_label.grid(row=3, column=0, pady=(10, 0), sticky="e")

# entries
website_entry = Entry(frame, width=21)
website_entry.grid(row=1, column=1, pady=(10, 0), sticky="w")
email_entry = Entry(frame, width=35)
email_entry.grid(row=2, column=1, columnspan=2, pady=(10, 0), sticky="w")
password_entry = Entry(frame, width=20)
password_entry.grid(row=3, column=1, pady=(10, 0), sticky="w")

# buttons
password_button = Button(frame, text="Generate Password", command=generate_password, font=("Helvetica", 9, "bold"),
                         cursor="hand2")
password_button.grid(row=3, column=2, pady=(10, 0))

add_button = Button(frame, text="Add", width=36, command=save, font=("Helvetica", 10, "bold"), cursor="hand2",
                    bg="#00ff00", fg="black")
add_button.grid(row=4, column=1, columnspan=2, pady=(10, 0))
search_button = Button(frame, text="Search", width=15, command=find_password, font=("Helvetica", 9, "bold"),
                       cursor="hand2")
search_button.grid(column=2, row=1, pady=(10, 0), padx=(5, 0))

# Explicitly set the font for labels
website_label.config(font=("Helvetica", 11))
email_label.config(font=("Helvetica", 11))
password_label.config(font=("Helvetica", 11))

# Explicitly set the font for entry widgets
website_entry.config(font=("Helvetica", 11))
email_entry.config(font=("Helvetica", 11))
password_entry.config(font=("Helvetica", 11))

window.mainloop()
