class Book:
    def __init__(self, title, author, year, isbn, is_borrowed=None, borrower=None, borrow_date=None):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.is_borrowed = is_borrowed  # Default to False
        self.borrower = borrower  # Default to None
        self.borrow_date = borrow_date

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year}) - ISBN: {self.isbn} - {f'Borrowed on {self.borrow_date}' if self.is_borrowed else 'Available'}"
