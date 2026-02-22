LIBRARY MANAGEMENT SYSTEM
- Desktop Library Management System using Python, PySide6 and MySQL

A full-featured desktop Library Management System built using Python, PySide6 (Qt for Python), and MySQL.
This application provides a structured graphical interface to manage books, students, professors, employees, and the complete borrowing and return workflow with fine tracking.

FEATURES:

Books Management:

• Add/remove new books

• View all books in a table format

• Track book availability status

• Store ISBN, topics and price

Students Management:

• Add/remove student details

• Store department and class

• Track pending fines

Professors Management:

• Add/remove professor records

• Track fines

• Department-wise management

Employees Management:

• Add/remoev library staff

• Manage issuing authority


Borrow and Return System:

• Issue books to students or professors

• Automatic due date generation

• Fine tracking system

• Return book processing

• Search by Borrower ID

• Search by Staff ID

• Search by Book ID


GUI Features:

• Multi-window structured navigation

• Table headings for all datasets

• Centered dashboard layout

• Dropdown borrower type selector

• Grid-based aligned forms

• Clean and structured UI design

TECH STACK:

• Python 3.x

• PySide6 (Qt for Python)
https://doc.qt.io/qtforpython/

• MySQL


INSTALLATION:

1. Clone the Repository
git clone https://github.com/KhanMdAyan/Library-Database-System.git

3. Create Virtual Environment (Recommended)
  python -m venv venv
* Activate (Windows):
  venv\Scripts\activate

3. Install Dependencies(PySide6 and mysql connector)
pip install PySide6 mysql-connector-python

4. Setup MySQL Database
  Run schema.sql on your MySQL server
Update database credentials in config.py file
Make sure they match your MySQL configuration.
While you're at it, you can change email details too.

5. And that's it! Run the Application python main.py

FINE LOGIC:
Fines are calculated based on the books' price and depending on the borrower.

• Fine is calculated based on due date

• Fine updates when borrowed records are accessed

• Fine amount is stored in database

• Displayed inside borrowed table


FUTURE IMPROVEMENTS:

• Authentication system

• Export to CSV

• Sorting and filtering

• Reports dashboard

FOR CONTRIBUTION:

Fork the repository

Create a new branch

Make improvements

Submit a pull request

LICENSE:

This project is open-source and intended for learning and academic use.

AUTHOR: Ayan Khan
Desktop application built using PySide6 and MySQL.
