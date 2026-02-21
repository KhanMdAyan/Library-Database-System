from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QLabel, QMessageBox, QComboBox
)

from services.borrow_service import return_book, issue_book
from services.fine_service import run_daily_fine_update
from services.email_service import send_overdue_emails
from database.connection import get_connection


class BorrowedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Borrowed List")
        self.showMaximized()

        # Run daily systems automatically
        run_daily_fine_update()
        send_overdue_emails()

        main_layout = QHBoxLayout()
        right_layout = QVBoxLayout()
        

        self.table = QTableWidget()
        main_layout.addWidget(self.table, 3)
        main_layout.addLayout(right_layout, 1)

        # Search Borrower
        self.borrower_search = QLineEdit()
        self.borrower_search.setPlaceholderText("Search Borrower ID")
        right_layout.addWidget(self.borrower_search)

        self.borrower_btn = QPushButton("Search Borrower")
        right_layout.addWidget(self.borrower_btn)

        # Search Staff
        self.staff_search = QLineEdit()
        self.staff_search.setPlaceholderText("Search Staff ID")
        right_layout.addWidget(self.staff_search)

        self.staff_btn = QPushButton("Search Staff")
        right_layout.addWidget(self.staff_btn)

        # Search Book
        self.book_search = QLineEdit()
        self.book_search.setPlaceholderText("Search Book ID")
        right_layout.addWidget(self.book_search)

        self.book_btn = QPushButton("Search Book")
        right_layout.addWidget(self.book_btn)
        # -------- ISSUE SECTION --------

        self.issue_book_id = QLineEdit()
        self.issue_book_id.setPlaceholderText("Book ID")

        self.issue_staff_id = QLineEdit()
        self.issue_staff_id.setPlaceholderText("Issuing Staff ID")

        self.issue_borrower_id = QLineEdit()
        self.issue_borrower_id.setPlaceholderText("Borrower ID")

        self.issue_type_dropdown = QComboBox()
        self.issue_type_dropdown.addItems(["Student", "Professor"])

        self.issue_btn = QPushButton("Issue Book")

        right_layout.addWidget(self.issue_book_id)
        right_layout.addWidget(self.issue_staff_id)
        right_layout.addWidget(self.issue_borrower_id)
        right_layout.addWidget(self.issue_type_dropdown)
        right_layout.addWidget(self.issue_btn)
        # Return Section
        self.return_staff_input = QLineEdit()
        self.return_staff_input.setPlaceholderText("Receiving Staff ID")
        right_layout.addWidget(self.return_staff_input)

        self.return_btn = QPushButton("Mark as Returned")
        right_layout.addWidget(self.return_btn)

        self.total_label = QLabel("")
        right_layout.addWidget(self.total_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.borrower_btn.clicked.connect(self.search_borrower)
        self.staff_btn.clicked.connect(self.search_staff)
        self.book_btn.clicked.connect(self.search_book)
        self.return_btn.clicked.connect(self.return_selected)
        self.issue_btn.clicked.connect(self.issue_book_action)

        self.load_all()

    # ------------------ LOAD ALL ------------------

    def load_all(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM borrowed
            ORDER BY issued_date DESC
        """)

        records = cursor.fetchall()
        conn.close()

        self.populate_table(records)

    # ------------------ POPULATE TABLE ------------------

    def populate_table(self, records):
        self.table.setRowCount(len(records))
        self.table.setColumnCount(len(records[0]) if records else 0)

        for row, record in enumerate(records):
            for col, value in enumerate(record):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    # ------------------ SEARCH BORROWER ------------------

    def search_borrower(self):
        borrower_id = self.borrower_search.text()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM borrowed
            WHERE issued_to_id=%s
            ORDER BY status='Borrowed' DESC, issued_date DESC
        """, (borrower_id,))

        records = cursor.fetchall()

        # Get total fine
        cursor.execute("""
            SELECT pending_fines FROM students WHERE student_id=%s
        """, (borrower_id,))
        student = cursor.fetchone()

        if not student:
            cursor.execute("""
                SELECT pending_fines FROM professors WHERE professor_id=%s
            """, (borrower_id,))
            student = cursor.fetchone()

        conn.close()

        total = student[0] if student else 0
        self.total_label.setText(f"Total Pending Fines: {total}")

        self.populate_table(records)

    # ------------------ SEARCH STAFF ------------------

    def search_staff(self):
        staff_id = self.staff_search.text()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM borrowed
            WHERE issued_by_staff_id=%s
               OR received_by_staff_id=%s
            ORDER BY issued_date DESC
        """, (staff_id, staff_id))

        records = cursor.fetchall()
        conn.close()

        self.total_label.setText("")
        self.populate_table(records)

    # ------------------ SEARCH BOOK ------------------

    def search_book(self):
        book_id = self.book_search.text()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM borrowed
            WHERE book_id=%s
            ORDER BY issued_date DESC
        """, (book_id,))

        records = cursor.fetchall()
        conn.close()

        self.total_label.setText("")
        self.populate_table(records)



    def issue_book_action(self):
        book_id = self.issue_book_id.text()
        staff_id = self.issue_staff_id.text()
        borrower_id = self.issue_borrower_id.text()
        borrower_type = self.issue_type_dropdown.currentText()
        result = issue_book(book_id, staff_id, borrower_id, borrower_type)

        QMessageBox.information(self, "Result", result)
        self.load_all()
        self.issue_type_dropdown.setCurrentIndex(0)

    # ------------------ RETURN ------------------

    def return_selected(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Error", "Select a record first")
            return

        borrow_id = self.table.item(row, 0).text()
        staff_id = self.return_staff_input.text()

        result = return_book(borrow_id, staff_id)

        QMessageBox.information(self, "Result", result)
        self.load_all()