import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import base64
import hashlib
import os

# 💡 Generate key from password
def generate_key(password):
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

# 🔒 Encrypt file
def encrypt_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    # 💪 Enforce strong password
    import re
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"\d", password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        
        messagebox.showwarning(
            "Weak Password ❗",
            "Please use a stronger password:\n"
            "• At least 8 characters\n"
            "• One uppercase & one lowercase letter\n"
            "• One number\n"
            "• One special character (!@#...)\n\n"
            "💡 Encryption aborted for your safety 💔"
        )
        return

    key = generate_key(password)
    fernet = Fernet(key)

    try:
        with open(filepath, 'rb') as file:
            data = file.read()
        encrypted = fernet.encrypt(data)

        with open(filepath + ".encrypted", 'wb') as enc_file:
            enc_file.write(encrypted)

        messagebox.showinfo("Success", f"File encrypted successfully!\nSaved as: {filepath}.encrypted")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to encrypt file: {e}")


# 🔓 Decrypt file
def decrypt_file():
    filepath = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.encrypted")])
    if not filepath:
        return

    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return
    

    key = generate_key(password)
    fernet = Fernet(key)

    try:
        with open(filepath, 'rb') as enc_file:
            encrypted = enc_file.read()
        decrypted = fernet.decrypt(encrypted)

        original_path = filepath.replace(".encrypted", ".decrypted")
        with open(original_path, 'wb') as dec_file:
            dec_file.write(decrypted)

        messagebox.showinfo("Success", f"File decrypted!\nSaved as: {original_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decrypt file: {e}")

# 🎀 GUI Setup
root = tk.Tk()
root.title("🔐 Secure File Encryption Tool by Nounou 💖")
root.geometry("500x300")
root.configure(bg="#f5f5f5")

tk.Label(root, text="Enter a strong password:", font=("Arial", 12), bg="#f5f5f5").pack(pady=10)
password_entry = tk.Entry(root, width=30, show="*", font=("Arial", 12))
password_entry.pack(pady=5)

encrypt_btn = tk.Button(root, text="🔒 Encrypt File", width=20, bg="#a5d6a7", font=("Arial", 11), command=encrypt_file)
encrypt_btn.pack(pady=15)

decrypt_btn = tk.Button(root, text="🔓 Decrypt File", width=20, bg="#ef9a9a", font=("Arial", 11), command=decrypt_file)
decrypt_btn.pack(pady=5)

root.mainloop()
