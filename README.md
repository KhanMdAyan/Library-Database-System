# 📚 Library Management System

Desktop Library Management System using Python, PySide6, and MySQL.

A full-featured desktop Library Management System built using Python,
PySide6 (Qt for Python), and MySQL.
This application provides a structured graphical interface to manage
books, students, professors, employees, and the complete borrowing and
return workflow with fine tracking.

------------------------------------------------------------------------

# 🛠 Tech Stack

-   Python 3.x
-   PySide6 (Qt for Python) – https://doc.qt.io/qtforpython/
-   MySQL

------------------------------------------------------------------------


# 📸 Preview:

* Main Window:


<img width="897" height="287" alt="image" src="https://github.com/user-attachments/assets/4eee341b-8c6d-498c-a352-2035d54d8ec9" />

* Books List Window:


<img width="406" height="689" alt="image" src="https://github.com/user-attachments/assets/d0f93648-b3dc-4601-ab55-ba257bf71cef" />


* Student List Window:


<img width="404" height="657" alt="image" src="https://github.com/user-attachments/assets/121a2b50-cb3e-48bc-a9da-fd8f09157864" />

* Borrowed List Window:


<img width="1920" height="1005" alt="image" src="https://github.com/user-attachments/assets/f58510d6-ba6d-4b84-b129-e1afc34f4118" />


------------------------------------------------------------------------

# 🚀 Features

📖 Books Management

-   Add/remove new books
-   View all books in a table format
-   Track book availability status
-   Store ISBN, topics, and price

🎓 Students Management

-   Add/remove student details
-   Store department and class
-   Track pending fines

👨‍🏫 Professors Management

-   Add/remove professor records
-   Track fines
-   Department-wise management

👨‍💼 Employees Management

-   Add/remove library staff
-   Manage issuing authority

🔄 Borrow and Return System

-   Issue books to students or professors
-   Automatic due date generation
-   Fine tracking system
-   Return book processing
-   Search by Borrower ID
-   Search by Staff ID
-   Search by Book ID

🖥 GUI Features

-   Multi-window structured navigation
-   Table headings for all datasets
-   Centered dashboard layout
-   Dropdown borrower type selector
-   Grid-based aligned forms
-   Clean and structured UI design


------------------------------------------------------------------------

# ⚙ Installation

1. Clone the Repository

git clone https://github.com/KhanMdAyan/Library-Database-System.git

2. Create Virtual Environment (Recommended)

4. Install Dependencies (PySide, mysql connector)

pip install PySide6 mysql-connector-python

5. Setup MySQL Database

-   Run schema.sql on your MySQL server
-   Update database credentials in config.py file
-   Make sure they match your MySQL configuration
-   You can also update email details there

# ▶ Run the Application

python main.py

------------------------------------------------------------------------

# 💰 Fine Logic

-   Fine is calculated based on due date
-   The value is set based on the books' price
-   Fine updates when borrowed records are accessed
-   Fine amount is stored in database
-   Displayed inside borrowed table
-   Fines are calculated based on the book’s price and borrower type

------------------------------------------------------------------------

# 🔮 Future Improvements

-   Authentication system
-   Export to CSV
-   Sorting and filtering
-   Reports dashboard

------------------------------------------------------------------------

# 🤝 Contribution

1.  Fork the repository
2.  Create a new branch
3.  Make improvements
4.  Submit a pull request

------------------------------------------------------------------------

# 📄 License

This project is open-source and intended for learning and academic use.

------------------------------------------------------------------------

# 👤 Author

Ayan Khan

📧 KhanMdAyan0@gmail.com

🔗 LinkedIn: https://www.linkedin.com/in/khanmdayan/

💻 GitHub: https://github.com/KhanMdAyan
