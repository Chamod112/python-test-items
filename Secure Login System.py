import tkinter as tk
from tkinter import messagebox

FILE = "users.txt"

def register():
    user = username.get()
    pwd = password.get()

    if user == "" or pwd == "":
        messagebox.showerror("Error", "All fields required")
        return

    with open(FILE, "a") as f:
        f.write(f"{user},{pwd}\n")

    messagebox.showinfo("Success", "Registered successfully")

def login():
    user = username.get()
    pwd = password.get()

    try:
        with open(FILE, "r") as f:
            for line in f:
                u, p = line.strip().split(",")
                if u == user and p == pwd:
                    messagebox.showinfo("Success", "Login Successful")
                    return
        messagebox.showerror("Error", "Invalid credentials")
    except:
        messagebox.showerror("Error", "No users found")

root = tk.Tk()
root.title("Secure Login System")
root.geometry("300x250")

tk.Label(root, text="Username").pack()
username = tk.Entry(root)
username.pack()

tk.Label(root, text="Password").pack()
password = tk.Entry(root, show="*")
password.pack()

tk.Button(root, text="Register", command=register).pack(pady=5)
tk.Button(root, text="Login", command=login).pack()

root.mainloop()
