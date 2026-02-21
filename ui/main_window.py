# The main window layout 




from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from ui.books_window import BooksWindow
from ui.employees_window import EmployeesWindow
from ui.students_window import StudentsWindow
from ui.professors_window import ProfessorsWindow
from ui.borrowed_window import BorrowedWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.setMinimumWidth(600) # This width is set because it wasn't showing the full window title. 

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.book_btn = QPushButton("Book List")
        self.employee_btn = QPushButton("Employee List")
        self.student_btn = QPushButton("Student List")
        self.prof_btn = QPushButton("Professor List")
        self.borrowed_btn = QPushButton("Borrowed List")


        #Putting fixed button length for better visuals
        self.book_btn.setFixedWidth(200)
        self.employee_btn.setFixedWidth(200)
        self.student_btn.setFixedWidth(200)
        self.prof_btn.setFixedWidth(200)
        self.borrowed_btn.setFixedWidth(200)

        layout.addWidget(self.book_btn)
        layout.addWidget(self.employee_btn)
        layout.addWidget(self.student_btn)
        layout.addWidget(self.prof_btn)
        layout.addWidget(self.borrowed_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.book_btn.clicked.connect(self.open_books)
        self.employee_btn.clicked.connect(self.open_employees)
        self.student_btn.clicked.connect(self.open_students)
        self.prof_btn.clicked.connect(self.open_professors)
        self.borrowed_btn.clicked.connect(self.open_borrowed)

    def open_books(self):
        self.books_window = BooksWindow()
        self.books_window.show()

    def open_employees(self):
        self.emp_window = EmployeesWindow()
        self.emp_window.show()

    def open_students(self):
        self.student_window = StudentsWindow()
        self.student_window.show()

    def open_professors(self):
        self.prof_window = ProfessorsWindow()
        self.prof_window.show()

    def open_borrowed(self):
        self.borrowed_window = BorrowedWindow()
        self.borrowed_window.show()