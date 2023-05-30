from tkinter import *
from tkinter import messagebox
import random
import json
FONT_NAME = "Verdana"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_pw():

    # Create lists of random letters, numbers, and symbols for the password
    random_letters = [random.choice(letters) for num in range(random.randint(8, 10))]
    random_numbers = [random.choice(numbers) for num in range(random.randint(2, 4))]
    random_symbols = [random.choice(symbols) for num in range(random.randint(2, 4))]

    # Combine the 3 lists above into one list and shuffle the order
    password_list = random_letters + random_symbols + random_numbers
    random.shuffle(password_list)

    # Convert the list into a string and populate in the "Password" field
    password = "".join(password_list)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():

    # Define the website, username, and password by pulling from the entry boxes
    website = website_entry.get()
    username = user_entry.get()
    password = password_entry.get()

    # Convert the above into a dictionary for the JSON format
    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    # Open the JSON file and txt and update with "new_data."
    # Will return error message if website, username, or password has no entry
    if 0 in (len(website), len(username), len(password)):
        messagebox.showwarning(title="Empty Entry", message="Please don't leave blanks")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            # Create new json and txt files with first entries
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
            with open("data.txt", mode="a") as pw_file:
                pw_file.write(f"\n{website} | {username} | {password}")
        else:
            # Update old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

            with open("data.txt", mode="a") as pw_file:
                pw_file.write(f"\n{website} | {username} | {password}")
        finally:
            user_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.delete(0, END)
            website_entry.focus()


# ---------------------------- Search Password ------------------------------- #

def search_pw():

    # Search JSON file for website entry and returns credentials
    website = website_entry.get().title()
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
    try:
        email = data[website]["email"]
        password = data[website]["password"]
    except KeyError:
        # Returns warning if credentials don't exist
        messagebox.showinfo(title="Credentials", message="No credentials for this website")
    else:
        messagebox.showinfo(title=f"{website} Credentials", message=f"Email: {email}"
                                                         f"\nPassword: {password}")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Set up the canvas with image
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Set up labels
website_label = Label(text="Website:", font=(FONT_NAME, 12))
website_label.grid(column=0, row=1)

user_label = Label(text="Email/Username:", font=(FONT_NAME, 12))
user_label.grid(column=0, row=2)

password_label = Label(text="Password:", font=(FONT_NAME, 12))
password_label.grid(column=0, row=3)

# Set up Buttons
generate_button = Button(text="Generate Password", font=(FONT_NAME, 10), width=19, command=generate_pw)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", font=(FONT_NAME, 12), width=36, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", font=(FONT_NAME, 10), width=19, command=search_pw)
search_button.grid(column=2, row=1)

# Set up Entries
website_entry = Entry(width=33)
website_entry.grid(column=1, row=1)
website_entry.focus()

user_entry = Entry(width=60)
user_entry.grid(column=1, row=2, columnspan=2)
user_entry.insert(0, "parkeraman10@gmail.com")

password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

window.mainloop()
