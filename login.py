import streamlit as st
import re
import os

USER_FILE = "users.txt"

# 📁 File Utilities
def load_users():
    """Load users from file into a dictionary {email: password}"""
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as f:
        lines = f.readlines()
    users = {}
    for line in lines:
        if ',' in line:
            email, password = line.strip().split(',', 1)
            users[email] = password
    return users

def save_user(email, password):
    """Append a new user to the file"""
    with open(USER_FILE, 'a') as f:
        f.write(f"{email},{password}\n")

# 📌 Validators
def is_valid_email(email):
    """Check valid email format"""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def is_valid_password(password):
    """Password must contain letters and numbers, at least 6 chars"""
    return (
        len(password) >= 6 and
        any(char.isdigit() for char in password) and
        any(char.isalpha() for char in password)
    )

# 📝 Registration Form
def register():
    st.subheader("📝 Register")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")
    confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Register"):
        users = load_users()
        if email in users:
            st.warning("Email already registered.")
        elif not is_valid_email(email):
            st.error("Invalid email format.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif not is_valid_password(password):
            st.error("Password must be at least 6 characters long and contain both letters and digits.")
        else:
            save_user(email, password)
            st.success("Account created successfully!")

# 🔐 Login Form
def login():
    st.subheader("🔐 Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        users = load_users()
        if email in users and users[email] == password:
            st.success(f"Welcome, {email}!")
        else:
            st.error("Invalid credentials!")

# 🚀 Main App
def main():
    st.title("Login & Register System (File-Based)")
    menu = st.selectbox("Menu", ["Login", "Register"])
    if menu == "Login":
        login()
    else:
        register()

if __name__ == "__main__":
    main()
