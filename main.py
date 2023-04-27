from tkinter import messagebox, Canvas, Tk, Label, Entry, Button, PhotoImage, END
import pyperclip

from data_manager import search_username_password, save_username_password, SaveToJsonException
from validations import is_required_field_valid, is_username_password_valid
from password_generator import generate_password


def create_password():
    password = generate_password()
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


def search():
    website = website_entry.get()
    username_password = search_username_password(website)

    if is_username_password_valid(username_password):
        password = username_password["password"]
        username = username_password["username"]

        pyperclip.copy(password)
        messagebox.showinfo(title=f"{website}", message=f"Username: {username}\n"
                                                        f"Password is copied to clipboard")
    else:
        messagebox.showinfo(title="Oops", message=f"User for the '{website}' not found")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get().lower()
    username = username_entry.get()
    password = password_entry.get()

    pw_data = {
        website: {
            "username": username,
            "password": password
        }
    }

    if not is_required_field_valid(website) or not is_required_field_valid(password):
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"The se are the details entered: \nEmail: {username} "
                                                              f"\nPassword: {password} \nIs it ok to save?")
        if not is_ok:
            return

        try:
            result = save_username_password(pw_data)

            if result is None:
                return

        except SaveToJsonException as stje:
            messagebox.showinfo(title="Oops", message=stje.message)
        else:
            username_entry.delete(0, END)
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="../pw_manager/logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

website_entry = Entry(width=26)
website_entry.grid(row=1, column=1, )

website_search_button = Button(text="Search", width=7, command=search)
website_search_button.grid(row=1, column=2)

username_label = Label(text="Email/Username:")
username_label.grid(row=2, column=0)

username_entry = Entry(width=37)
username_entry.grid(row=2, column=1, columnspan=2)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

password_entry = Entry(width=26)
password_entry.grid(row=3, column=1)

generate_password_button = Button(text="Generate", command=create_password, width=7)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Save", width=35, command=save)
add_button.grid(row=4, column=1, columnspan=2)

website_entry.focus()

window.mainloop()
