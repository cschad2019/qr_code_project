import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog, Toplevel
import qrcode
from PIL import ImageTk, Image
import re

# Global variables
is_premium = False
logged_in = False
uploaded_image_path = None

# Helper function to validate URLs
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

# Function to generate QR code
def generate_qr():
    if not logged_in:
        messagebox.showwarning("Login Required", "Please log in to generate a QR code.")
        return

    url = url_entry.get()
    shape = shape_var.get()

    if not is_valid_url(url):
        messagebox.showwarning("Input Error", "Please enter a valid URL.")
        return

    color = color_entry.get() if is_premium or color_entry.get() else "black"

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=color, back_color="white").convert("RGBA")

        # No shape mask applied
        img_with_shape = apply_shape_mask(img, shape)
        img_with_shape.save("qr_code.png")

        open_qr_window()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to apply shape mask
def apply_shape_mask(qr_image, shape):
    # Return the QR image as is without applying any shape mask
    return qr_image

# Function to open QR code window
def open_qr_window():
    qr_window = Toplevel(root)
    qr_window.title("Generated QR Code")
    qr_window.geometry("450x450")

    img = Image.open("qr_code.png")
    img = img.resize((400, 400))
    img_tk = ImageTk.PhotoImage(img)

    qr_label = tk.Label(qr_window, image=img_tk)
    qr_label.image = img_tk  # Keep a reference to avoid garbage collection
    qr_label.pack(pady=10)

# Function to handle login
def login():
    global logged_in
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "password":
        logged_in = True
        login_frame.pack_forget()  # Hide login frame
        app_frame.pack()  # Show the main app frame
        messagebox.showinfo("Login Success", "You have successfully logged in!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to reset fields
def reset_fields():
    url_entry.delete(0, tk.END)
    color_entry.delete(0, tk.END)
    shape_var.set("square")

# Function to sign up for premium
def sign_up_premium():
    global is_premium
    is_premium = True
    messagebox.showinfo("Premium Activated", "You now have access to premium features!")

# Root window setup
root = tk.Tk()
root.title("Style QR Code Generator")
root.geometry("400x500")
root.config(bg="#f7f7f7")

# Login frame
login_frame = tk.Frame(root, bg="#f7f7f7", padx=20, pady=20)
login_frame.pack(pady=40)

login_title = tk.Label(login_frame, text="Login", font=("Helvetica", 18, "bold"), bg="#f7f7f7")
login_title.grid(row=0, columnspan=2, pady=10)

username_label = tk.Label(login_frame, text="Username:", font=("Helvetica", 12), bg="#f7f7f7")
username_label.grid(row=1, column=0, pady=5, sticky="e")
username_entry = tk.Entry(login_frame, font=("Helvetica", 12))
username_entry.grid(row=1, column=1, pady=5)

password_label = tk.Label(login_frame, text="Password:", font=("Helvetica", 12), bg="#f7f7f7")
password_label.grid(row=2, column=0, pady=5, sticky="e")
password_entry = tk.Entry(login_frame, font=("Helvetica", 12), show="*")
password_entry.grid(row=2, column=1, pady=5)

login_button = tk.Button(login_frame, text="Login", command=login, bg="#007bff", fg="white", width=15)
login_button.grid(row=3, columnspan=2, pady=20)

# App frame
app_frame = tk.Frame(root, bg="#f7f7f7", padx=20, pady=20)

url_label = tk.Label(app_frame, text="Enter URL:", font=("Helvetica", 12), bg="#f7f7f7")
url_label.pack(pady=5)
url_entry = tk.Entry(app_frame, font=("Helvetica", 12), width=30)
url_entry.pack(pady=5)

color_label = tk.Label(app_frame, text="Choose Color:", font=("Helvetica", 12), bg="#f7f7f7")
color_label.pack(pady=5)
color_entry = tk.Entry(app_frame, font=("Helvetica", 12), width=30)
color_entry.pack(pady=5)

shape_var = tk.StringVar(value="square")
shape_label = tk.Label(app_frame, text="Choose Shape:", font=("Helvetica", 12), bg="#f7f7f7")
shape_label.pack(pady=5)

square_button = tk.Radiobutton(app_frame, text="Square", variable=shape_var, value="square", bg="#f7f7f7")
square_button.pack(pady=5)

circle_button = tk.Radiobutton(app_frame, text="Circle", variable=shape_var, value="circle", bg="#f7f7f7")
circle_button.pack(pady=5)

triangle_button = tk.Radiobutton(app_frame, text="Triangle", variable=shape_var, value="triangle", bg="#f7f7f7")
triangle_button.pack(pady=5)

generate_button = tk.Button(app_frame, text="Generate QR Code", command=generate_qr, bg="#007bff", fg="white")
generate_button.pack(pady=10)

premium_button = tk.Button(app_frame, text="Sign Up for Premium Features", command=sign_up_premium, bg="#28a745", fg="white")
premium_button.pack(pady=5)

reset_button = tk.Button(app_frame, text="Reset", command=reset_fields, bg="#ff5733", fg="white")
reset_button.pack(pady=10)

root.mainloop()
