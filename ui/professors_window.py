from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox
)

from services.professor_service import (
    get_all_professors,
    add_professor,
    delete_professor
)


class ProfessorsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professors List")

        layout = QVBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        self.dept_input = QLineEdit()
        self.dept_input.setPlaceholderText("Department")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        layout.addWidget(self.name_input)
        layout.addWidget(self.dept_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_input)

        self.add_btn = QPushButton("Add Professor")
        self.delete_btn = QPushButton("Remove Professor")

        layout.addWidget(self.add_btn)
        layout.addWidget(self.delete_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.add_btn.clicked.connect(self.add_professor)
        self.delete_btn.clicked.connect(self.remove_professor)

        self.load_data()

    def load_data(self):
        professors = get_all_professors()
        self.table.setRowCount(len(professors))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Department",
            "Phone", "Email", "Pending Fines"
        ])

        for row, prof in enumerate(professors):
            for col, value in enumerate(prof):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def add_professor(self):
        add_professor(
            self.name_input.text(),
            self.dept_input.text(),
            self.phone_input.text(),
            self.email_input.text()
        )
        self.load_data()
        self.name_input.clear()
        self.dept_input.clear()
        self.phone_input.clear()
        self.email_input.clear()

    def remove_professor(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Select a professor first")
            return

        professor_id = self.table.item(row, 0).text()
        delete_professor(professor_id)
        self.load_data()