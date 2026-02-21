from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QLabel, QMessageBox
)

from services.student_service import get_all_students, add_student, delete_student


class StudentsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Students List")

        layout = QVBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Input fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        self.dept_input = QLineEdit()
        self.dept_input.setPlaceholderText("Department")

        self.class_input = QLineEdit()
        self.class_input.setPlaceholderText("Class")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        layout.addWidget(self.name_input)
        layout.addWidget(self.dept_input)
        layout.addWidget(self.class_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_input)

        self.add_btn = QPushButton("Add Student")
        self.delete_btn = QPushButton("Remove Student")

        layout.addWidget(self.add_btn)
        layout.addWidget(self.delete_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.add_btn.clicked.connect(self.add_student)
        self.delete_btn.clicked.connect(self.remove_student)

        self.load_data()

    def load_data(self):
        students = get_all_students()
        self.table.setRowCount(len(students))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Department", "Class",
            "Phone", "Email", "Pending Fines"
        ])

        for row, student in enumerate(students):
            for col, value in enumerate(student):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def add_student(self):
        add_student(
            self.name_input.text(),
            self.dept_input.text(),
            self.class_input.text(),
            self.phone_input.text(),
            self.email_input.text()
        )
        self.load_data()

    def remove_student(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Select a student first")
            return

        student_id = self.table.item(row, 0).text()
        delete_student(student_id)
        self.load_data()