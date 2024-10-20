# user.py
import csv
import os

class User:
    def __init__(self, username, password, is_admin = False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

class UserManager:
    def __init__(self, filename='users.csv'):
        self.filename = filename
        self.users = {}
        self.load_users()  # Load users from the CSV file
        self.ensure_admin()  # Ensure the admin user exists

    def load_users(self):
        """Load users from a CSV file."""
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    username, password, is_admin = row
                    self.users[username] = User(username, password, is_admin == 'True')

    def ensure_admin(self):
        """Ensure the admin user exists."""
        if "admin" not in self.users:
            self.users["admin"] = User("admin", "adminpass", is_admin=True)
            self.save_users()  # Save the admin user to the CSV

    def validate_user(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        return None

    def add_user(self, username, password):
        if username in self.users:
            return False  # Username already exists
        self.users[username] = User(username, password)
        self.save_users()  # Save users to CSV after adding a new one
        return True  # User added successfully

    def save_users(self):
        """Save users to a CSV file."""
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for username, user in self.users.items():
                writer.writerow([username, user.password, user.is_admin])

    def change_password(self, username, new_password):
        """Change the password for the specified user."""
        if username in self.users:
            # Update the password (consider hashing it)
            # self.users[username]['password'] = new_password
            self.users[username] = User(username, new_password)
            self.save_users()
            return True
        return False
