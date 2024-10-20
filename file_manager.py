import csv
from book import Book

class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def load_books(self):
        books = []
        try:
            with open(self.filename) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Create a Book object from the row data
                    books.append(Book(**row))
        except (FileNotFoundError, csv.Error):
            return []  # Return an empty list if file not found or error occurs
        return books

    def save_books(self, books):
        with open(self.filename, mode='w', newline='') as f:
            # Define the fieldnames (the keys of the Book object)
            fieldnames = ['title', 'author', 'year', 'isbn', 'is_borrowed', 'borrower', 'borrow_date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()  # Write the header
            for book in books:
                writer.writerow(book.__dict__)  # Write each book's attributes as a row
