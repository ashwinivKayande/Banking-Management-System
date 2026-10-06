import json
import os
from datetime import datetime

DATA_FILE = "accounts.json"


# Load accounts from JSON file
def load_accounts():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except:
            return {}
    return {}


# Save accounts to JSON file
def save_accounts():
    with open(DATA_FILE, "w") as file:
        json.dump(accounts, file, indent=4)


accounts = load_accounts()


def create_account():
    print("\n========== CREATE ACCOUNT ========== - banking_system.py:29")

    account_number = input("Enter account number: ").strip()

    if account_number in accounts:
        print("Account already exists! - banking_system.py:34")
        return

    name = input("Enter your name: ").strip()
    pin = input("Set a 4-digit PIN: ").strip()

    if len(pin) != 4 or not pin.isdigit():
        print("PIN must be exactly 4 digits. - banking_system.py:41")
        return

    accounts[account_number] = {
        "name": name,
        "pin": pin,
        "balance": 0.0,
        "transactions": []
    }

    save_accounts()

    print("\nAccount created successfully! - banking_system.py:53")
    print("Account Number: - banking_system.py:54", account_number)
    print("Account Holder: - banking_system.py:55", name)
    print("Balance: ₹0.00 - banking_system.py:56")


def login():
    print("\n========== LOGIN ========== - banking_system.py:60")

    account_number = input("Enter account number: ").strip()
    pin = input("Enter PIN: ").strip()

    if account_number not in accounts:
        print("Account not found! - banking_system.py:66")
        return None

    if accounts[account_number]["pin"] != pin:
        print("Incorrect PIN! - banking_system.py:70")
        return None

    print("Login successful! - banking_system.py:73")
    return account_number


def deposit(account_number):
    print("\n========== DEPOSIT MONEY ========== - banking_system.py:78")

    try:
        amount = float(input("Enter deposit amount: ₹"))

        if amount <= 0:
            print("Enter a valid amount. - banking_system.py:84")
            return

        accounts[account_number]["balance"] += amount

        accounts[account_number]["transactions"].append({
            "type": "Deposit",
            "amount": amount,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

        save_accounts()

        print("Money deposited successfully! - banking_system.py:97")
        print("Current Balance: ₹{:.2f} - banking_system.py:98".format(
            accounts[account_number]["balance"]
        ))

    except ValueError:
        print("Please enter a valid number. - banking_system.py:103")


def withdraw(account_number):
    print("\n========== WITHDRAW MONEY ========== - banking_system.py:107")

    try:
        amount = float(input("Enter withdrawal amount: ₹"))

        if amount <= 0:
            print("Enter a valid amount. - banking_system.py:113")
            return

        if amount > accounts[account_number]["balance"]:
            print("Insufficient balance! - banking_system.py:117")
            return

        accounts[account_number]["balance"] -= amount

        accounts[account_number]["transactions"].append({
            "type": "Withdrawal",
            "amount": amount,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

        save_accounts()

        print("Money withdrawn successfully! - banking_system.py:130")
        print("Current Balance: ₹{:.2f} - banking_system.py:131".format(
            accounts[account_number]["balance"]
        ))

    except ValueError:
        print("Please enter a valid number. - banking_system.py:136")


def check_balance(account_number):
    print("\n========== ACCOUNT DETAILS ========== - banking_system.py:140")

    account = accounts[account_number]

    print("Account Number: - banking_system.py:144", account_number)
    print("Account Holder: - banking_system.py:145", account["name"])
    print("Balance: ₹{:.2f} - banking_system.py:146".format(account["balance"]))


def transfer_money(account_number):
    print("\n========== MONEY TRANSFER ========== - banking_system.py:150")

    receiver = input("Enter receiver account number: ").strip()

    if receiver not in accounts:
        print("Receiver account not found! - banking_system.py:155")
        return

    if receiver == account_number:
        print("You cannot transfer money to the same account. - banking_system.py:159")
        return

    try:
        amount = float(input("Enter transfer amount: ₹"))

        if amount <= 0:
            print("Enter a valid amount. - banking_system.py:166")
            return

        if amount > accounts[account_number]["balance"]:
            print("Insufficient balance! - banking_system.py:170")
            return

        accounts[account_number]["balance"] -= amount
        accounts[receiver]["balance"] += amount

        date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        accounts[account_number]["transactions"].append({
            "type": "Transfer Sent",
            "amount": amount,
            "to": receiver,
            "date": date
        })

        accounts[receiver]["transactions"].append({
            "type": "Transfer Received",
            "amount": amount,
            "from": account_number,
            "date": date
        })

        save_accounts()

        print("Money transferred successfully! - banking_system.py:194")
        print("Transferred: ₹{:.2f} - banking_system.py:195".format(amount))
        print("Current Balance: ₹{:.2f} - banking_system.py:196".format(
            accounts[account_number]["balance"]
        ))

    except ValueError:
        print("Please enter a valid number. - banking_system.py:201")


def transaction_history(account_number):
    print("\n========== TRANSACTION HISTORY ========== - banking_system.py:205")

    transactions = accounts[account_number]["transactions"]

    if not transactions:
        print("No transactions found. - banking_system.py:210")
        return

    for i, transaction in enumerate(transactions, start=1):

        print("\nTransaction - banking_system.py:215", i)
        print("Type: - banking_system.py:216", transaction["type"])
        print("Amount: ₹{:.2f} - banking_system.py:217".format(transaction["amount"]))

        if "to" in transaction:
            print("To Account: - banking_system.py:220", transaction["to"])

        if "from" in transaction:
            print("From Account: - banking_system.py:223", transaction["from"])

        print("Date: - banking_system.py:225", transaction["date"])


def user_menu(account_number):

    while True:

        print("\n======================================== - banking_system.py:232")
        print("USER MENU - banking_system.py:233")
        print("======================================== - banking_system.py:234")
        print("1. Deposit Money - banking_system.py:235")
        print("2. Withdraw Money - banking_system.py:236")
        print("3. Check Balance - banking_system.py:237")
        print("4. Transfer Money - banking_system.py:238")
        print("5. Transaction History - banking_system.py:239")
        print("6. Logout - banking_system.py:240")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            deposit(account_number)

        elif choice == "2":
            withdraw(account_number)

        elif choice == "3":
            check_balance(account_number)

        elif choice == "4":
            transfer_money(account_number)

        elif choice == "5":
            transaction_history(account_number)

        elif choice == "6":
            print("Logged out successfully. - banking_system.py:260")
            break

        else:
            print("Invalid choice! - banking_system.py:264")


def main():

    while True:

        print("\n - banking_system.py:271")
        print("======================================== - banking_system.py:272")
        print("BANKING SYSTEM - banking_system.py:273")
        print("======================================== - banking_system.py:274")
        print("1. Create Account - banking_system.py:275")
        print("2. Login - banking_system.py:276")
        print("3. Exit - banking_system.py:277")
        print("======================================== - banking_system.py:278")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_account()

        elif choice == "2":

            account_number = login()

            if account_number is not None:
                user_menu(account_number)

        elif choice == "3":

            print("\nThank you for using Banking System! - banking_system.py:294")
            print("Goodbye! - banking_system.py:295")
            break

        else:
            print("Invalid choice! Please try again. - banking_system.py:299")


if __name__ == "__main__":
    main()