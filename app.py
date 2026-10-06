import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "accounts.json"


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Banking Management System",
    page_icon="🏦",
    layout="wide"
)


# -----------------------------
# DATA FUNCTIONS
# -----------------------------
def load_accounts():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except:
            return {}
    return {}


def save_accounts(accounts):
    with open(DATA_FILE, "w") as file:
        json.dump(accounts, file, indent=4)


# -----------------------------
# SESSION STATE
# -----------------------------
if "accounts" not in st.session_state:
    st.session_state.accounts = load_accounts()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account_number" not in st.session_state:
    st.session_state.account_number = None


# -----------------------------
# HEADER
# -----------------------------
st.title("🏦 Banking Management System")
st.caption("Secure and simple digital banking management application")


# =========================================================
# LOGIN / SIGNUP PAGE
# =========================================================

if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Create Account"])

    # -------------------------
    # LOGIN
    # -------------------------
    with tab1:

        st.subheader("Login to Your Account")

        account_number = st.text_input(
            "Account Number",
            key="login_account"
        )

        pin = st.text_input(
            "4-Digit PIN",
            type="password",
            key="login_pin"
        )

        if st.button("Login", use_container_width=True):

            accounts = st.session_state.accounts

            if account_number not in accounts:
                st.error("Account not found.")

            elif accounts[account_number]["pin"] != pin:
                st.error("Incorrect PIN.")

            else:
                st.session_state.logged_in = True
                st.session_state.account_number = account_number

                st.success("Login successful!")
                st.rerun()

    # -------------------------
    # CREATE ACCOUNT
    # -------------------------
    with tab2:

        st.subheader("Create New Bank Account")

        new_account = st.text_input(
            "Account Number",
            key="new_account"
        )

        name = st.text_input(
            "Account Holder Name",
            key="new_name"
        )

        new_pin = st.text_input(
            "Create 4-Digit PIN",
            type="password",
            key="new_pin"
        )

        confirm_pin = st.text_input(
            "Confirm PIN",
            type="password",
            key="confirm_pin"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            accounts = st.session_state.accounts

            if not new_account or not name or not new_pin:
                st.warning("Please fill all fields.")

            elif new_account in accounts:
                st.error("Account already exists.")

            elif not new_pin.isdigit() or len(new_pin) != 4:
                st.error("PIN must contain exactly 4 digits.")

            elif new_pin != confirm_pin:
                st.error("PINs do not match.")

            else:

                accounts[new_account] = {
                    "name": name,
                    "pin": new_pin,
                    "balance": 0.0,
                    "transactions": []
                }

                save_accounts(accounts)

                st.session_state.accounts = accounts

                st.success(
                    f"Account created successfully! "
                    f"Your account number is {new_account}."
                )


# =========================================================
# DASHBOARD
# =========================================================

else:

    accounts = st.session_state.accounts
    account_number = st.session_state.account_number
    account = accounts[account_number]

    # -------------------------
    # SIDEBAR
    # -------------------------

    with st.sidebar:

        st.header("🏦 Banking System")

        st.write("Welcome,")

        st.subheader(account["name"])

        st.divider()

        st.write("Account Number")
        st.code(account_number)

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.account_number = None
            st.rerun()

    # -------------------------
    # DASHBOARD
    # -------------------------

    st.subheader("📊 Account Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Available Balance",
            f"₹{account['balance']:,.2f}"
        )

    with col2:
        st.metric(
            "📜 Total Transactions",
            len(account["transactions"])
        )

    with col3:
        st.metric(
            "👤 Account Number",
            account_number
        )

    st.divider()

    # -------------------------
    # OPERATIONS
    # -------------------------

    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 Deposit",
        "💸 Withdraw",
        "🔄 Transfer",
        "📜 Transactions"
    ])

    # =====================================================
    # DEPOSIT
    # =====================================================

    with tab1:

        st.subheader("Deposit Money")

        amount = st.number_input(
            "Enter Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key="deposit_amount"
        )

        if st.button(
            "Deposit Money",
            use_container_width=True
        ):

            if amount <= 0:
                st.error("Enter a valid amount.")

            else:

                account["balance"] += amount

                account["transactions"].append({
                    "type": "Deposit",
                    "amount": amount,
                    "date": datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )
                })

                save_accounts(accounts)

                st.success(
                    f"₹{amount:,.2f} deposited successfully!"
                )

                st.rerun()

    # =====================================================
    # WITHDRAW
    # =====================================================

    with tab2:

        st.subheader("Withdraw Money")

        amount = st.number_input(
            "Enter Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key="withdraw_amount"
        )

        if st.button(
            "Withdraw Money",
            use_container_width=True
        ):

            if amount <= 0:
                st.error("Enter a valid amount.")

            elif amount > account["balance"]:
                st.error("Insufficient balance.")

            else:

                account["balance"] -= amount

                account["transactions"].append({
                    "type": "Withdrawal",
                    "amount": amount,
                    "date": datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )
                })

                save_accounts(accounts)

                st.success(
                    f"₹{amount:,.2f} withdrawn successfully!"
                )

                st.rerun()

    # =====================================================
    # TRANSFER
    # =====================================================

    with tab3:

        st.subheader("Transfer Money")

        receiver = st.text_input(
            "Receiver Account Number"
        )

        amount = st.number_input(
            "Transfer Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key="transfer_amount"
        )

        if st.button(
            "Transfer Money",
            use_container_width=True
        ):

            if receiver not in accounts:
                st.error("Receiver account not found.")

            elif receiver == account_number:
                st.error(
                    "You cannot transfer money to your own account."
                )

            elif amount <= 0:
                st.error("Enter a valid amount.")

            elif amount > account["balance"]:
                st.error("Insufficient balance.")

            else:

                account["balance"] -= amount
                accounts[receiver]["balance"] += amount

                date = datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )

                account["transactions"].append({
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

                save_accounts(accounts)

                st.success(
                    f"₹{amount:,.2f} transferred successfully!"
                )

                st.rerun()

    # =====================================================
    # TRANSACTION HISTORY
    # =====================================================

    with tab4:

        st.subheader("Transaction History")

        transactions = account["transactions"]

        if not transactions:

            st.info("No transactions available.")

        else:

            for i, transaction in enumerate(
                reversed(transactions),
                start=1
            ):

                with st.container(border=True):

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.write(
                            f"**{transaction['type']}**"
                        )

                    with col2:
                        st.write(
                            f"₹{transaction['amount']:,.2f}"
                        )

                    with col3:
                        st.write(
                            transaction["date"]
                        )

                    if "to" in transaction:
                        st.caption(
                            f"To Account: {transaction['to']}"
                        )

                    if "from" in transaction:
                        st.caption(
                            f"From Account: {transaction['from']}"
                        )


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "Banking Management System | "
    "Developed using Python & Streamlit"
)