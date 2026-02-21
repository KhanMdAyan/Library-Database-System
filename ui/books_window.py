from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QLabel
)

from services.book_service import (
    get_all_books,
    add_book,
    delete_book,
    search_book_by_id_or_isbn
)

from database.connection import get_connection


class BooksWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Books List")

        layout = QVBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Inputs
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Book Title")

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Book Topics")

        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("ISBN")

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Book Price")

        layout.addWidget(self.title_input)
        layout.addWidget(self.topic_input)
        layout.addWidget(self.isbn_input)
        layout.addWidget(self.price_input)

        # Buttons
        self.add_btn = QPushButton("Add Book")
        self.delete_btn = QPushButton("Remove Book")

        layout.addWidget(self.add_btn)
        layout.addWidget(self.delete_btn)

        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Book ID or ISBN")

        self.search_btn = QPushButton("Search Book")

        layout.addWidget(self.search_input)
        layout.addWidget(self.search_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connections
        self.add_btn.clicked.connect(self.add_book)
        self.delete_btn.clicked.connect(self.remove_book)
        self.search_btn.clicked.connect(self.search_book)

        self.load_data()

    # ---------------- LOAD ALL BOOKS ----------------

    def load_data(self):
        books = get_all_books()

        self.table.setRowCount(len(books))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Book ID", "Title", "Topics",
            "ISBN", "Price", "Status"
        ])

        for row, book in enumerate(books):
            for col, value in enumerate(book):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    # ---------------- ADD BOOK ----------------

    def add_book(self):
        try:
            price = float(self.price_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid price")
            return

        add_book(
            self.title_input.text(),
            self.topic_input.text(),
            self.isbn_input.text(),
            price
        )

        self.load_data()

    # ---------------- REMOVE BOOK ----------------

    def remove_book(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Select a book first")
            return

        book_id = self.table.item(row, 0).text()
        delete_book(book_id)
        self.load_data()

    # ---------------- SEARCH ----------------

    def search_book(self):
        value = self.search_input.text()
        result = search_book_by_id_or_isbn(value)

        if not result:
            QMessageBox.information(self, "Search", "No book found")
            return

        self.table.setRowCount(len(result))
        self.table.setColumnCount(6)

        for row, book in enumerate(result):
            for col, value in enumerate(book):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))