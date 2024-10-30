import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime
from typing import Dict, List

class ATM_GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Python ATM")
        self.window.geometry("800x600")
        self.window.configure(bg="#f0f0f0")

        # Initialize ATM backend
        self.accounts_file = "accounts.json"
        self.transactions_file = "transactions.json"
        self.current_user = None
        self.load_data()

        # Create and show login frame
        self.create_styles()
        self.create_frames()
        self.show_login_frame()

        # Center window
        self.center_window()

    def create_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure common styles
        style.configure('Custom.TFrame', background='#f0f0f0')
        style.configure('Custom.TLabel', background='#f0f0f0', font=('Arial', 12))
        style.configure('Custom.TButton', 
                       font=('Arial', 12),
                       padding=10,
                       background='#4CAF50')
        style.configure('Header.TLabel',
                       font=('Arial', 16, 'bold'),
                       background='#f0f0f0')
        style.configure('Title.TLabel',
                       font=('Arial', 24, 'bold'),
                       background='#f0f0f0')

    def create_frames(self):
        # Login Frame
        self.login_frame = ttk.Frame(self.window, style='Custom.TFrame')
        self.create_login_widgets()

        # Register Frame
        self.register_frame = ttk.Frame(self.window, style='Custom.TFrame')
        self.create_register_widgets()

        # Forgot Password Frame
        self.forgot_frame = ttk.Frame(self.window, style='Custom.TFrame')
        self.create_forgot_widgets()

        # Main Menu Frame
        self.menu_frame = ttk.Frame(self.window, style='Custom.TFrame')
        self.create_menu_widgets()

        # Transaction Frames
        self.balance_frame = ttk.Frame(self.window, style='Custom.TFrame')
        self.withdraw_frame = ttk.Frame(self.window, style='Custom.TFrame')
        self.deposit_frame = ttk.Frame(self.window, style='Custom.TFrame')
        self.history_frame = ttk.Frame(self.window, style='Custom.TFrame')

        self.create_transaction_widgets()

    def create_login_widgets(self):
        # Title
        ttk.Label(self.login_frame, 
                 text="Welcome to Python ATM",
                 style='Title.TLabel').pack(pady=20)

        # Account Number
        ttk.Label(self.login_frame,
                 text="Account Number:",
                 style='Custom.TLabel').pack(pady=5)
        self.account_entry = ttk.Entry(self.login_frame, font=('Arial', 12))
        self.account_entry.pack(pady=5)

        # PIN
        ttk.Label(self.login_frame,
                 text="PIN:",
                 style='Custom.TLabel').pack(pady=5)
        self.pin_entry = ttk.Entry(self.login_frame, show="*", font=('Arial', 12))
        self.pin_entry.pack(pady=5)

        # Login Button
        ttk.Button(self.login_frame,
                  text="Login",
                  style='Custom.TButton',
                  command=self.login).pack(pady=10)

        # Register and Forgot Password Links
        ttk.Button(self.login_frame, 
                  text="Register", 
                  style='Custom.TButton', 
                  command=self.show_register_frame).pack(pady=5)
        ttk.Button(self.login_frame, 
                  text="Forgot Username/Password", 
                  style='Custom.TButton', 
                  command=self.show_forgot_frame).pack(pady=5)

    def create_register_widgets(self):
        # Title
        ttk.Label(self.register_frame, 
                 text="Register New Account",
                 style='Title.TLabel').pack(pady=20)

        # Account Number, PIN and Name Entries
        ttk.Label(self.register_frame, text="Account Number:", style='Custom.TLabel').pack(pady=5)
        self.reg_account_entry = ttk.Entry(self.register_frame, font=('Arial', 12))
        self.reg_account_entry.pack(pady=5)

        ttk.Label(self.register_frame, text="PIN:", style='Custom.TLabel').pack(pady=5)
        self.reg_pin_entry = ttk.Entry(self.register_frame, show="*", font=('Arial', 12))
        self.reg_pin_entry.pack(pady=5)

        ttk.Label(self.register_frame, text="Full Name:", style='Custom.TLabel').pack(pady=5)
        self.reg_name_entry = ttk.Entry(self.register_frame, font=('Arial', 12))
        self.reg_name_entry.pack(pady=5)

        # Register Button
        ttk.Button(self.register_frame, 
                  text="Register", 
                  style='Custom.TButton', 
                  command=self.register).pack(pady=10)
        ttk.Button(self.register_frame, 
                  text="Back to Login", 
                  style='Custom.TButton', 
                  command=self.show_login_frame).pack(pady=5)

    def create_forgot_widgets(self):
        # Title
        ttk.Label(self.forgot_frame, 
                 text="Forgot Username or Password",
                 style='Title.TLabel').pack(pady=20)

        # Account Recovery Information
        ttk.Label(self.forgot_frame, text="Enter Full Name:", style='Custom.TLabel').pack(pady=5)
        self.forgot_name_entry = ttk.Entry(self.forgot_frame, font=('Arial', 12))
        self.forgot_name_entry.pack(pady=5)

        # Recovery Button
        ttk.Button(self.forgot_frame, 
                  text="Recover", 
                  style='Custom.TButton', 
                  command=self.recover_account).pack(pady=10)
        ttk.Button(self.forgot_frame, 
                  text="Back to Login", 
                  style='Custom.TButton', 
                  command=self.show_login_frame).pack(pady=5)

    def create_menu_widgets(self):
        # Title with Welcome Message
        self.welcome_label = ttk.Label(self.menu_frame,
                                     text="Welcome",
                                     style='Title.TLabel')
        self.welcome_label.pack(pady=20)

        # Menu Buttons
        buttons = [
            ("Check Balance", self.show_balance_frame),
            ("Withdraw", self.show_withdraw_frame),
            ("Deposit", self.show_deposit_frame),
            ("Transaction History", self.show_history_frame),
            ("Logout", self.logout)
        ]

        for text, command in buttons:
            ttk.Button(self.menu_frame,
                      text=text,
                      style='Custom.TButton',
                      command=command).pack(pady=10, padx=20, fill=tk.X)

    def create_transaction_widgets(self):
        # Balance Frame
        ttk.Label(self.balance_frame,
                 text="Current Balance",
                 style='Header.TLabel').pack(pady=20)
        self.balance_label = ttk.Label(self.balance_frame,
                                     text="",
                                     style='Title.TLabel')
        self.balance_label.pack(pady=20)
        ttk.Button(self.balance_frame,
                  text="Back to Menu",
                  style='Custom.TButton',
                  command=self.show_menu_frame).pack(pady=20)

        # Withdraw Frame
        ttk.Label(self.withdraw_frame,
                 text="Withdraw Money",
                 style='Header.TLabel').pack(pady=20)
        self.withdraw_entry = ttk.Entry(self.withdraw_frame, font=('Arial', 12))
        self.withdraw_entry.pack(pady=10)
        ttk.Button(self.withdraw_frame,
                  text="Withdraw",
                  style='Custom.TButton',
                  command=self.perform_withdrawal).pack(pady=10)
        ttk.Button(self.withdraw_frame,
                  text="Back to Menu",
                  style='Custom.TButton',
                  command=self.show_menu_frame).pack(pady=10)

        # Deposit Frame
        ttk.Label(self.deposit_frame,
                 text="Deposit Money",
                 style='Header.TLabel').pack(pady=20)
        self.deposit_entry = ttk.Entry(self.deposit_frame, font=('Arial', 12))
        self.deposit_entry.pack(pady=10)
        ttk.Button(self.deposit_frame,
                  text="Deposit",
                  style='Custom.TButton',
                  command=self.perform_deposit).pack(pady=10)
        ttk.Button(self.deposit_frame,
                  text="Back to Menu",
                  style='Custom.TButton',
                  command=self.show_menu_frame).pack(pady=10)

        # History Frame
        ttk.Label(self.history_frame,
                 text="Transaction History",
                 style='Header.TLabel').pack(pady=20)
        self.history_text = tk.Text(self.history_frame,
                                  height=15,
                                  width=50,
                                  font=('Arial', 10))
        self.history_text.pack(pady=10)
        ttk.Button(self.history_frame,
                  text="Back to Menu",
                  style='Custom.TButton',
                  command=self.show_menu_frame).pack(pady=10)

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def load_data(self):
        # Create default data if files don't exist
        if not os.path.exists(self.accounts_file):
            self.accounts = {}
            self.save_accounts()
        else:
            with open(self.accounts_file, 'r') as f:
                self.accounts = json.load(f)

        if not os.path.exists(self.transactions_file):
            self.transactions = {}
            self.save_transactions()
        else:
            with open(self.transactions_file, 'r') as f:
                self.transactions = json.load(f)

    def save_accounts(self):
        with open(self.accounts_file, 'w') as f:
            json.dump(self.accounts, f, indent=4)

    def save_transactions(self):
        with open(self.transactions_file, 'w') as f:
            json.dump(self.transactions, f, indent=4)

    def login(self):
        account = self.account_entry.get()
        pin = self.pin_entry.get()

        if account in self.accounts and self.accounts[account]["pin"] == pin:
            self.current_user = account
            self.welcome_label.config(text=f"Welcome, {self.accounts[account]['name']}")
            self.show_menu_frame()
            self.account_entry.delete(0, tk.END)
            self.pin_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid account number or PIN")

    def logout(self):
        self.current_user = None
        self.show_login_frame()

    def show_frame(self, frame):
        for f in [self.login_frame, self.register_frame, self.forgot_frame, 
                  self.menu_frame, self.balance_frame, self.withdraw_frame, 
                  self.deposit_frame, self.history_frame]:
            f.pack_forget()
        frame.pack(fill=tk.BOTH, expand=True)

    def show_login_frame(self): self.show_frame(self.login_frame)
    def show_register_frame(self): self.show_frame(self.register_frame)
    def show_forgot_frame(self): self.show_frame(self.forgot_frame)
    def show_menu_frame(self): self.show_frame(self.menu_frame)
    
    def show_balance_frame(self):
        self.balance_label.config(text=f"₹{self.accounts[self.current_user]['balance']:.2f}")
        self.show_frame(self.balance_frame)

    def show_withdraw_frame(self):
        self.withdraw_entry.delete(0, tk.END)
        self.show_frame(self.withdraw_frame)

    def show_deposit_frame(self):
        self.deposit_entry.delete(0, tk.END)
        self.show_frame(self.deposit_frame)

    def show_history_frame(self):
        self.history_text.delete(1.0, tk.END)
        history = self.get_transaction_history()
        if not history:
            self.history_text.insert(tk.END, "No transactions found.")
        else:
            for transaction in history:
                self.history_text.insert(tk.END, 
                    f"Type: {transaction['type'].capitalize()}\n"
                    f"Amount: ₹{abs(transaction['amount']):.2f}\n"
                    f"Balance: ₹{transaction['balance']:.2f}\n"
                    f"Time: {transaction['timestamp']}\n"
                    f"{'-'*30}\n")
        self.show_frame(self.history_frame)

    def perform_withdrawal(self):
        try:
            amount = float(self.withdraw_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Please enter a positive amount")
                return
            
            if amount > self.accounts[self.current_user]["balance"]:
                messagebox.showerror("Error", "Insufficient funds")
                return

            self.accounts[self.current_user]["balance"] -= amount
            self.log_transaction("withdrawal", -amount)
            self.save_accounts()
            
            messagebox.showinfo("Success", 
                f"Successfully withdrew ₹{amount:.2f}\n"
                f"New balance: ₹{self.accounts[self.current_user]['balance']:.2f}")
            
            self.show_menu_frame()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def perform_deposit(self):
        try:
            amount = float(self.deposit_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Please enter a positive amount")
                return

            self.accounts[self.current_user]["balance"] += amount
            self.log_transaction("deposit", amount)
            self.save_accounts()
            
            messagebox.showinfo("Success", 
                f"Successfully deposited ₹{amount:.2f}\n"
                f"New balance: ₹{self.accounts[self.current_user]['balance']:.2f}")
            
            self.show_menu_frame()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def register(self):
        account = self.reg_account_entry.get()
        pin = self.reg_pin_entry.get()
        name = self.reg_name_entry.get()

        if not account or not pin or not name:
            messagebox.showerror("Error", "All fields are required")
            return

        if account in self.accounts:
            messagebox.showerror("Error", "Account already exists")
            return

        self.accounts[account] = {
            "pin": pin,
            "balance": 0.0,
            "name": name
        }
        self.save_accounts()
        messagebox.showinfo("Success", "Account registered successfully")
        self.show_login_frame()

    def recover_account(self):
        name = self.forgot_name_entry.get()
        matching_accounts = [
            (acc, data) for acc, data in self.accounts.items() if data['name'] == name
        ]

        if matching_accounts:
            message = "\n".join([f"Account: {acc}, PIN: {data['pin']}" for acc, data in matching_accounts])
            messagebox.showinfo("Account Recovery", message)
        else:
            messagebox.showerror("Error", "No accounts found for the given name")

    def log_transaction(self, transaction_type: str, amount: float):
        if self.current_user not in self.transactions:
            self.transactions[self.current_user] = []

        transaction = {
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance": self.accounts[self.current_user]["balance"]
        }
        self.transactions[self.current_user].append(transaction)
        self.save_transactions()

    def get_transaction_history(self) -> List[Dict]:
        if self.current_user and self.current_user in self.transactions:
            return self.transactions[self.current_user]
        return []

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    atm = ATM_GUI()
    atm.run()
