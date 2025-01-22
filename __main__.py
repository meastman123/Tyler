import tkinter as tk
import sqlite3
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk

# Main window for the register and login buttons
main_window = tk.Tk()
main_window.title("Bike Shop - Login/Register")
main_window.geometry("400x400")  # Set window size


# Function to register a user
def register_user():
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    if username and password and email:
        conn = sqlite3.connect('shoes_shop.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                       (username, password, email))
        conn.commit()
        conn.close()
        messagebox.showinfo("Registration", "Registration Successful!")
        register_window.destroy()  # Close the register window
    else:
        messagebox.showwarning("Input error", "All fields are required!")


# Function to open the register window
def open_register_window():
    global register_window, username_entry, password_entry, email_entry

    register_window = tk.Toplevel()
    register_window.title("Register")
    register_window.geometry('400x300')

    tk.Label(register_window, text="Username").pack(pady=5)
    username_entry = tk.Entry(register_window)
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Password").pack(pady=5)
    password_entry = tk.Entry(register_window, show='*')
    password_entry.pack(pady=5)

    tk.Label(register_window, text="Email").pack(pady=5)
    email_entry = tk.Entry(register_window)
    email_entry.pack(pady=5)

    tk.Button(register_window, text="Register", command=register_user).pack(pady=10)


# Function to log in a user
def login_user(main_window):
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('shoes_shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Login", "Login Successful!")
        login_window.destroy()  # Close the login window
        main_window.destroy()   # Close the main window
        open_shop_window()      # Open the shop window
    else:
        messagebox.showwarning("Login", "Invalid username or password")


# Function to open the login window
def open_login_window(main_window):
    global login_window, username_entry, password_entry

    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry('300x200')

    tk.Label(login_window, text="Username").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password").pack(pady=5)
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=lambda: login_user(main_window)).pack(pady=10)


# Function to open the shop window
def open_shop_window():
    shop_window = tk.Tk()  # Create a new main window for the shop
    shop_window.title("Bike Shop - Available Bikes and parts")
    shop_window.geometry("800x600")  # Adjust size to fit images

    tk.Label(shop_window, text="Select a product to add to your basket:", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(shop_window, text="Bikes:", font=("Helvetica", 16)).pack(pady=10)

    # List of shoes with their details
    shoes = [
        {"name": "Red bike", "price": 200, "image": "sneakers.jpg", "category": "bikes"},
        {"name": "Blue bike", "price": 120, "image": "boots.jpg",  "category": "bikes"},
        {"name": "Green bike", "price": 100, "image": "sandals.jpg", "category": "bikes"},
    ]

    bikeParts = [
        {"name": "Red bike", "price": 50, "image": "loafers.jpg", "category": "bike parts"},
        {"name": "Blue bike", "price": 40, "image": "heels.jpg", "category": "bike parts"},
        {"name": "Green bike", "price": 30, "image": "flipflops.jpg", "category": "bike parts"},
    ]

    basket = []  # To hold items added to the basket

    # Create a frame to hold the shoe selection
    frame = tk.Frame(shop_window)
    frame.pack()

    def add_to_basket(shoe):
        basket.append(shoe)
        messagebox.showinfo("Basket", f"Added {shoe['name']} to basket!")

    # Iterate over the shoes and create widgets
    for index, shoe in enumerate(shoes):
        # Load and resize image
        image = Image.open(shoe["image"])
        image = image.resize((150, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Create a frame for each shoe and place it in a grid
        frame_shoe = tk.Frame(frame)
        frame_shoe.grid(row=index // 1, column=index % 3, padx=10, pady=10)  # Arrange in a 3-column row
        tk.Label(shop_window, text="Bike parts:", font=("Helvetica", 16)).pack(pady=10)
        frame_bP = tk.Frame(frame)
        frame_bikeParts.grid(row=index // 1, column= index % 3, padx=10, pady=10) # Arrange in a 3 column row


        label = tk.Label(frame_shoe, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack()

        tk.Label(frame_shoe, text=f"{shoe['name']} - ${shoe['price']}").pack()

        tk.Button(frame_shoe, text="Add to Basket", command=lambda s=shoe: add_to_basket(s)).pack()

    # Purchase button
    tk.Button(shop_window, text="View Basket", command=lambda: view_basket(basket)).pack(pady=20)


# Function to view the basket
def view_basket(basket):
    basket_window = tk.Toplevel()
    basket_window.title("Your Basket")
    basket_window.geometry("400x400")

    tk.Label(basket_window, text="Your Basket", font=("Helvetica", 16)).pack(pady=10)

    total_price = 0
    for shoe in basket:
        tk.Label(basket_window, text=f"{shoe['name']} - ${shoe['price']}").pack()
        total_price += shoe['price']

    tk.Label(basket_window, text=f"Total: ${total_price}", font=("Helvetica", 14)).pack(pady=10)

    tk.Button(basket_window, text="Purchase", command=lambda: complete_purchase(basket, basket_window, total_price)).pack(pady=20)


# Function to complete purchase
def complete_purchase(basket, basket_window, total_price):
    if total_price > 0:
        messagebox.showinfo("Login", "Login Successful!")
        open_payment_window(basket)
    else:
        messagebox.showwarning("Basket", "You don't have anything in your basket")
        open_basket_window()  # Close the basket window



# Function to open the payment window
def open_payment_window(basket):
    payment_window = tk.Toplevel()
    payment_window.title("Payment")
    payment_window.geometry("400x500")

    tk.Label(payment_window, text="Review Your Order", font=("Helvetica", 16)).pack(pady=10)

    total_price = 0
    for shoe in basket:
        tk.Label(payment_window, text=f"{shoe['name']} - ${shoe['price']}").pack()
        total_price += shoe['price']

    tk.Label(payment_window, text=f"Total: ${total_price}", font=("Helvetica", 14)).pack(pady=10)

    tk.Label(payment_window, text="Enter Payment Details", font=("Helvetica", 14)).pack(pady=10)

    tk.Label(payment_window, text="Card Number").pack(pady=5)
    card_number_entry = tk.Entry(payment_window)
    card_number_entry.pack(pady=5)

    tk.Label(payment_window, text="Expiration Date (MM/YY)").pack(pady=5)
    expiration_entry = tk.Entry(payment_window)
    expiration_entry.pack(pady=5)

    tk.Label(payment_window, text="CVV").pack(pady=5)
    cvv_entry = tk.Entry(payment_window, show='*')
    cvv_entry.pack(pady=5)

    def confirm_payment():
        card_number = card_number_entry.get()
        expiration_date = expiration_entry.get()
        cvv = cvv_entry.get()

        if card_number and expiration_date and cvv:
            messagebox.showinfo("Payment", "Payment Successful! Thank you for your purchase.")
            payment_window.destroy()  # Close the payment window
        else:
            messagebox.showwarning("Input Error", "All fields are required!")

    tk.Button(payment_window, text="Confirm Payment", command=confirm_payment).pack(pady=20)



# Insert the Image of the shop
image = Image.open("shop.jpg")
image = image.resize((250, 150), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

image_label = tk.Label(main_window, image=photo)
image_label.pack(pady=10)

tk.Label(main_window, text="Welcome to the Bike Shop", font=("Helvetica", 16)).pack(pady=10)

Register_button = tk.Button(main_window, text="Register", width=15, command=open_register_window)
Register_button.pack(pady=10)

Login_button = tk.Button(main_window, text="Login", width=15, command=lambda: open_login_window(main_window))
Login_button.pack(pady=10)

main_window.mainloop()
