import os
import json
import getpass
import hashlib
import random
import argparse
from cryptography.fernet import Fernet

# Define the path to the password storage file
PASSWORD_FILE = "passwords.json"

# Check if the password storage file exists, and create it if it doesn't
if not os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, "w") as file:
        json.dump({}, file)

# Define functions for encryption and decryption
def generate_key(password):
    """Generate an encryption key based on the user's password."""
    password = password.encode()
    key = hashlib.sha256(password).digest()
    return key

def encrypt(data, key):
    """Encrypt data using Fernet symmetric encryption."""
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def decrypt(encrypted_data, key):
    """Decrypt data using Fernet symmetric encryption."""
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

def save_password(service, username, password, key):
    """Save a password in the password storage file."""
    with open(PASSWORD_FILE, "r") as file:
        passwords = json.load(file)
    
    # Encrypt the password before saving it
    encrypted_password = encrypt(password, key)
    passwords[service] = {"username": username, "password": encrypted_password}
    
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file)

def get_password(service, key):
    """Retrieve a password from the password storage file."""
    with open(PASSWORD_FILE, "r") as file:
        passwords = json.load(file)
    
    if service in passwords:
        encrypted_password = passwords[service]["password"]
        decrypted_password = decrypt(encrypted_password, key)
        return decrypted_password
    else:
        return None

def generate_random_password(length=12):
    """Generate a random password with a specified length."""
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_-+=<>?"
    password = "".join([random.choice(characters) for _ in range(length)])
    return password

def main():
    parser = argparse.ArgumentParser(description="PasswordWizardScript - A user-friendly password manager and generator.")
    parser.add_argument("--help", action="help", help="Show this help message and exit.")
    args = parser.parse_args()

    print("Welcome to PasswordWizardScript!")
    password = getpass.getpass("Enter your master password: ")
    key = generate_key(password)
    
    while True:
        print("\nMenu:")
        print("1. Store a new password")
        print("2. Retrieve a password")
        print("3. Generate a random password")
        print("4. Exit")
        
        choice = input("Enter your choice (1/2/3/4): ")
        
        if choice == "1":
            service = input("Enter the service name: ")
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            save_password(service, username, password, key)
            print("Password saved successfully!")
        
        elif choice == "2":
            service = input("Enter the service name: ")
            password = get_password(service, key)
            if password:
                print(f"Password for {service}: {password}")
            else:
                print("Password not found.")
        
        elif choice == "3":
            length = int(input("Enter the length of the password: "))
            password = generate_random_password(length)
            print(f"Generated password: {password}")
        
        elif choice == "4":
            print("Exiting PasswordWizardScript. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
