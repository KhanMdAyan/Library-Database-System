CREATE DATABASE library_db;
USE library_db;

-- Students table
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(100),
    class VARCHAR(50),
    phone_number VARCHAR(20),
    email VARCHAR(100),
    pending_fines DECIMAL(10,2) DEFAULT 0
) AUTO_INCREMENT=10000;

-- Professors table
CREATE TABLE professors (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(100),
    pending_fines DECIMAL(10,2) DEFAULT 0
) AUTO_INCREMENT=20000;

-- Staff table
CREATE TABLE library_staff (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(100)
) AUTO_INCREMENT=30000;

-- BOOKS
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    book_title VARCHAR(200),
    book_topics VARCHAR(200),
    isbn VARCHAR(50),
    book_price DECIMAL(10,2),
    status ENUM('Available','Borrowed') DEFAULT 'Available'
) AUTO_INCREMENT=40000;

-- Book tracking table
CREATE TABLE borrowed (
    borrow_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    book_name VARCHAR(200),
    issued_by_staff_id INT,
    issued_to_id INT,
    issued_to_type ENUM('Student','Professor'),
    issued_date DATE,
    due_date DATE,
    return_date DATE,
    pending_fines DECIMAL(10,2) DEFAULT 0,
    last_fine_update_date DATE,
    last_email_sent_date DATE,
    status ENUM('Borrowed','Returned') DEFAULT 'Borrowed',
    received_by_staff_id INT,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (issued_by_staff_id) REFERENCES library_staff(employee_id),
    FOREIGN KEY (received_by_staff_id) REFERENCES library_staff(employee_id)
);
