from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox
)

from services.staff_service import (
    get_all_staff,
    add_staff,
    delete_staff
)


class EmployeesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Staff List")

        layout = QVBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        layout.addWidget(self.name_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_input)

        self.add_btn = QPushButton("Add Employee")
        self.delete_btn = QPushButton("Remove Employee")

        layout.addWidget(self.add_btn)
        layout.addWidget(self.delete_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.add_btn.clicked.connect(self.add_employee)
        self.delete_btn.clicked.connect(self.remove_employee)

        self.load_data()

    def load_data(self):
        staff = get_all_staff()
        self.table.setRowCount(len(staff))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Employee ID", "Name", "Phone", "Email"
        ])

        for row, emp in enumerate(staff):
            for col, value in enumerate(emp):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def add_employee(self):
        add_staff(
            self.name_input.text(),
            self.phone_input.text(),
            self.email_input.text()
        )
        self.load_data()
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()

    def remove_employee(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Select an employee first")
            return

        employee_id = self.table.item(row, 0).text()
        delete_staff(employee_id)
        self.load_data()