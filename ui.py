import tkinter as tk
from tkinter import messagebox, simpledialog
from book import Book
from user import UserManager
from file_manager import FileManager
from tkinter import font
from datetime import datetime


class LibraryUI:
    def __init__(self, root):
        self.root = root
        self.user_manager = UserManager()
        self.current_user = None
        self.file_manager = FileManager("books.csv")
        self.books = []
        self.filtered_items = self.books.copy()
        self.filtered_books=[]
        self.colour1 = "#030C26" #bg
        self.colour2 = "#27418C" #text colour
        self.colour3 = "#6387F2" #textbox colour
        self.colour4 = "#0DF205"
        # Set up the main window
        self.root.title("Library Management System")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry("1080x720")
        self.root.state('zoomed')
        self.root.configure(bg=self.colour1, padx=20, pady=20)
        self.custom_font = font.Font(family="Arial", size=20, weight="bold")
        self.login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Username", font=self.custom_font, bg=self.colour1, fg=self.colour2).grid(row=0, column=0,
                                                                                                     padx=10, pady=10,
                                                                                                     sticky='w')
        self.username_entry = tk.Entry(self.root, font=self.custom_font, bg=self.colour3, fg=self.colour2)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Password label and entry
        tk.Label(self.root, text="Password", font=self.custom_font, bg=self.colour1, fg=self.colour2).grid(row=1, column=0,
                                                                                                     padx=10, pady=10,
                                                                                                     sticky='w')
        self.password_entry = tk.Entry(self.root, show='*', font=self.custom_font, bg=self.colour3, fg=self.colour2)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        # Login button
        tk.Button(self.root, text="Login", command=self.login, font=self.custom_font, bg=self.colour4, fg=self.colour1).grid(
            row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Add Borrower button
        tk.Button(self.root, text="Add Borrower", command=self.add_user, font=self.custom_font, bg=self.colour4,
                  fg=self.colour1).grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Make the layout responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.current_user = self.user_manager.validate_user(username, password)

        if self.current_user:
            self.load_books()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    def logout(self):
        """Logout the current user and return to the login screen."""
        self.current_user = None
        self.login_screen()

    def add_user(self):
        """Add a new borrower user."""
        username = simpledialog.askstring("Input", "Enter new borrower's username:", parent=self.root)
        password = simpledialog.askstring("Input", "Enter new borrower's password:", show='*', parent=self.root)

        if username and password:
            if self.user_manager.add_user(username, password):
                messagebox.showinfo("Success", "Borrower added successfully.")
            else:
                messagebox.showwarning("Error", "Username already exists.")
        else:
            messagebox.showwarning("Input Error", "Both fields must be filled out.")

    def load_books(self):
        """Load books from the file and display them."""
        self.clear_window()
        self.books = self.file_manager.load_books()

        # Search bar
        tk.Label(self.root, text="Search:", font=self.custom_font, bg=self.colour1, fg=self.colour2).grid(row=0, column=0,padx=10, pady=10,sticky='w',columnspan=1)
        self.search_entry = tk.Entry(self.root, font=self.custom_font, bg=self.colour3, fg=self.colour2)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        tk.Button(self.root, text="Search", command=self.search_books, font=self.custom_font, bg=self.colour4,
                  fg=self.colour1).grid(row=0, column=2, padx=10, pady=10, sticky='ew')
        self.borrowedOnlyVar = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(self.root, text='Borrowed Only', variable=self.borrowedOnlyVar, command=self.update_list, bg=self.colour4, font=self.custom_font, padx=10, fg=self.colour1)
        self.checkbox.grid(row=0, column=4)
        # Listbox to display books
        self.listbox = tk.Listbox(self.root, width=70, height=10, font=self.custom_font,
                                  bg=self.colour3, fg=self.colour2, selectbackground=self.colour4, selectforeground=self.colour1)
        self.listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        self.listbox2 = tk.Listbox(self.root, width=20, height=10, font=self.custom_font,
                                   bg=self.colour3, fg=self.colour2, selectbackground=self.colour4, selectforeground=self.colour1)
        self.listbox2.grid(row=1, column=4, columnspan=1, padx=10, pady=10, sticky='nsew')

        # Sync the scrolling of the two listboxes
        self.listbox.bind('<MouseWheel>', lambda event: self.on_mouse_wheel(event, self.listbox, self.listbox2))
        self.listbox2.bind('<MouseWheel>', lambda event: self.on_mouse_wheel(event, self.listbox2, self.listbox))

        # Admin buttons for adding/removing books
        if self.current_user.is_admin:
            tk.Button(self.root, text="Add Book", command=self.add_book, font=self.custom_font, bg=self.colour4,
                      fg=self.colour1).grid(row=2, column=0, padx=10, pady=5, sticky='ew',columnspan=2)
            tk.Button(self.root, text="Remove Book", command=self.remove_book, font=self.custom_font, bg=self.colour4,
                      fg=self.colour1).grid(row=2, column=2, padx=10, pady=5, sticky='ew',columnspan=3)

            # Borrow button for regular users
        tk.Button(self.root, text="Borrow Book", command=self.borrow_book, font=self.custom_font, bg=self.colour4,
                  fg=self.colour1).grid(row=3, column=0, padx=10, pady=5, sticky='ew',columnspan=2)

        # Return and logout buttons
        tk.Button(self.root, text="Return Book", command=self.return_book, font=self.custom_font, bg=self.colour4,
                  fg=self.colour1).grid(row=3, column=2, padx=10, pady=5, sticky='ew', columnspan=3)
        tk.Button(self.root, text="Logout", command=self.logout, font=self.custom_font, bg=self.colour4,
                  fg=self.colour1).grid(row=4, columnspan=5, padx=10, pady=10, sticky='ew')
        tk.Button(self.root, text="Change Password", command=self.change_password, font=self.custom_font,
                  bg=self.colour4,
                  fg=self.colour1).grid(row=5, columnspan=5, padx=10, pady=10, sticky='ew')

        # Load the list of books
        self.update_list()
        self.load_book_list()

        # Make the listbox responsive
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def on_mouse_wheel(self, event, source_listbox, target_listbox):
        source_listbox.yview_scroll(int(-1 * (event.delta / 120)), "units")
        target_listbox.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def change_password(self):
        current_password = simpledialog.askstring("Current Password", "Enter your current password:", show='*',
                                                  parent=self.root)
        new_password = simpledialog.askstring("New Password", "Enter your new password:", show='*', parent=self.root)

        if current_password and new_password:
            if self.user_manager.validate_user(self.current_user.username, current_password):
                if self.user_manager.change_password(self.current_user.username, new_password):
                    messagebox.showinfo("Success", "Password changed successfully.")
                else:
                    messagebox.showwarning("Error", "Failed to change password. Please try again.")
            else:
                messagebox.showwarning("Error", "Current password is incorrect.")
        else:
            messagebox.showwarning("Input Error", "Both fields must be filled out.")

    def load_book_list(self):
        self.listbox.delete(0, tk.END)
        self.listbox2.delete(0, tk.END)

        for book in self.filtered_items:
            self.listbox.insert(tk.END, str(book))
        for book in self.filtered_items:
            self.listbox2.insert(tk.END, str('Borrowed' if 'Borrowed' in str(book) else 'Available'))

    def update_list(self):
        if self.borrowedOnlyVar.get():
            self.filtered_items = [book for book in self.books if book.is_borrowed]
        else:
            self.filtered_items = self.books.copy()
        self.load_book_list()

    def search_books(self):
        search_query = self.search_entry.get().lower()
        self.update_list()
        self.load_book_list()
        self.filtered_books = [book for book in self.books if search_query in book.title.lower() or search_query in book.author.lower()]
        if self.borrowedOnlyVar.get():
            self.filtered_books = [book for book in self.filtered_books if book.is_borrowed]
        self.listbox.delete(0, tk.END)
        self.listbox2.delete(0, tk.END)

        for book in self.filtered_books:
            self.listbox.insert(tk.END, str(book))
        for book in self.filtered_books:
            self.listbox2.insert(tk.END, str('Borrowed' if 'Borrowed' in str(book) else 'Available'))

        if not self.filtered_books:
            messagebox.showinfo("No Results", "No books found matching your search.")

    def add_book(self):
        if not self.current_user.is_admin:
            messagebox.showwarning("Permission Denied", "You do not have permission to add books.")
            return

        title = simpledialog.askstring("Input", "Enter book title:", parent=self.root)
        author = simpledialog.askstring("Input", "Enter author:", parent=self.root)
        year = simpledialog.askstring("Input", "Enter year:", parent=self.root)
        isbn = simpledialog.askstring("Input", "Enter ISBN:", parent=self.root)

        if title and author and year and isbn:
            new_book = Book(title, author, year, isbn)
            self.books.append(new_book)
            self.file_manager.save_books(self.books)
            self.load_book_list()
        else:
            messagebox.showwarning("Input Error", "All fields must be filled out.")

    def remove_book(self):
        if not self.current_user.is_admin:
            messagebox.showwarning("Permission Denied", "You do not have permission to remove books.")
            return

        try:
            selected_index = self.listbox.curselection()[0]
            if len(self.filtered_books)>=(selected_index+1):
                # book is self.filtered_books[selected_index]
                # remove book in self.books
                book_name = (self.filtered_books[selected_index]).title
                for index, i in enumerate(self.books):
                    if i.title ==book_name:
                        print(i)
                        del self.books[index]
                del self.filtered_books[selected_index]
            else:
                del self.books[selected_index]

            self.file_manager.save_books(self.books)
            self.update_list()
            self.load_book_list()
        except IndexError:
            messagebox.showwarning("Selection Error", "No book selected.")

    def borrow_book(self):
        try:
            selected_index = self.listbox.curselection()[0]
            if len(self.filtered_books)>=(selected_index+1):
                book = self.filtered_books[selected_index]
            else:
                book= self.books[selected_index]
            if book.is_borrowed:
                messagebox.showinfo("Borrow Error", "This book is already borrowed.")
            else:
                book.is_borrowed= True
                book.borrower = self.current_user.username  # Track the borrower
                book.borrow_date = datetime.now().date()
                self.file_manager.save_books(self.books)
                self.load_book_list()
                messagebox.showinfo("Borrow", "Book borrowed successfully")

        except IndexError:
            messagebox.showwarning("Selection Error", "No book selected.")

    def return_book(self):
        try:
            selected_index = self.listbox.curselection()[0]
            if len(self.filtered_books) >= (selected_index + 1):
                book = self.filtered_books[selected_index]
            elif len(self.filtered_items) > 0:
                book = self.filtered_items[selected_index]
            else:
                book = self.books[selected_index]
                
            if not book.is_borrowed:
                messagebox.showinfo("Return Error", "This book is not currently borrowed.")
            elif book.borrower != self.current_user.username and not self.current_user.is_admin:
                messagebox.showinfo("Return Error", "You can only return books you borrowed.")
            else:
                book.is_borrowed = None
                book.borrower = None  # Clear the borrower
                book.borrow_date = None
                self.file_manager.save_books(self.books)
                self.update_list()
                self.load_book_list()
                messagebox.showinfo("Book Return", "Book returned successfully")
        except IndexError:
            messagebox.showwarning("Selection Error", "No book selected.")
