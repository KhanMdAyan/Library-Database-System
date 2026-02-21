# The borrowing logic and working behind the borrow list window.
# I've set the borrow limit for students as five books and for professors ten books
# It checks for book availability, validates everyone's IDs, sets due date, calculates fine,
# and updates borrower's data, book's data once it is returned


from datetime import date, timedelta
from database.connection import get_connection
from services.student_service import update_student_fine
from services.professor_service import update_professor_fine

def issue_book(book_id, staff_id, borrower_id, borrower_type):
    conn = get_connection()
    cursor = conn.cursor()

    # Validating Book avaliability
    cursor.execute("SELECT book_title, book_price, status FROM books WHERE book_id=%s", (book_id,))
    book = cursor.fetchone()

    if not book:
        conn.close()
        return "Book does not exist"

    book_name, book_price, status = book

    if status == "Borrowed":
        conn.close()
        return "Book is already borrowed"

    # Validating Staff ID
    cursor.execute("SELECT * FROM library_staff WHERE employee_id=%s", (staff_id,))
    if not cursor.fetchone():
        conn.close()
        return "Invalid staff ID"

    #Validating Borrower
    if borrower_type == "Student":
        cursor.execute("SELECT * FROM students WHERE student_id=%s", (borrower_id,))
        if not cursor.fetchone():
            conn.close()
            return "Invalid student ID"

        # Borrow limit check (5 books)
        cursor.execute("""
            SELECT COUNT(*) FROM borrowed
            WHERE issued_to_id=%s AND issued_to_type='Student' AND status='Borrowed'
        """, (borrower_id,))
        count = cursor.fetchone()[0]

        if count >= 5:
            conn.close()
            return "Student reached borrow limit (5)"

        due_date = date.today() + timedelta(days=7)

    elif borrower_type == "Professor":
        cursor.execute("SELECT * FROM professors WHERE professor_id=%s", (borrower_id,))
        if not cursor.fetchone():
            conn.close()
            return "Invalid professor ID"

        # Borrow limit check (10 books)
        cursor.execute("""
            SELECT COUNT(*) FROM borrowed
            WHERE issued_to_id=%s AND issued_to_type='Professor' AND status='Borrowed'
        """, (borrower_id,))
        count = cursor.fetchone()[0]

        if count >= 10:
            conn.close()
            return "Professor reached borrow limit (10)"

        due_date = date.today() + timedelta(days=30)

    else:
        conn.close()
        return "Invalid borrower type"

    # Register the books in db
    cursor.execute("""
        INSERT INTO borrowed (
            book_id,
            book_name,
            issued_by_staff_id,
            issued_to_id,
            issued_to_type,
            issued_date,
            due_date,
            last_fine_update_date,
            last_email_sent_date
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        book_id,
        book_name,
        staff_id,
        borrower_id,
        borrower_type,
        date.today(),
        due_date,
        date.today(),
        date.today()
    ))

    # Update the book status in books table after it is borrowed
    cursor.execute("UPDATE books SET status='Borrowed' WHERE book_id=%s", (book_id,))

    conn.commit()
    conn.close()

    return "Book issued successfully"



def return_book(borrow_id, receiving_staff_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if the borrow record exists
    cursor.execute("""
        SELECT book_id, issued_to_id, issued_to_type,
               due_date, pending_fines, status
        FROM borrowed
        WHERE borrow_id=%s
    """, (borrow_id,))
    record = cursor.fetchone()

    if not record:
        conn.close()
        return "Borrow record not found"

    book_id, borrower_id, borrower_type, due_date, current_fine, status = record

    if status == "Returned":
        conn.close()
        return "Book already returned"

    # Validate library staff that is receiving the book
    cursor.execute("SELECT * FROM library_staff WHERE employee_id=%s", (receiving_staff_id,))
    if not cursor.fetchone():
        conn.close()
        return "Invalid receiving staff ID"

    today = date.today()

    # Calculate remaining fine, if overdue
    additional_fine = 0

    if today > due_date:
        days_overdue = (today - due_date).days

        # Get book price
        cursor.execute("SELECT book_price FROM books WHERE book_id=%s", (book_id,))
        price = cursor.fetchone()[0]

        if borrower_type == "Student":
            daily_fine = price * 0.02
        else:
            daily_fine = price * 0.05

        additional_fine = daily_fine * days_overdue

    total_fine = current_fine + additional_fine

    # Once the book is returned the overdue fine is considered to be paid, hence subtract fine from borrower's total fine
    if borrower_type == "Student":
        update_student_fine(borrower_id, -total_fine)
    else:
        update_professor_fine(borrower_id, -total_fine)

    # Update borrowed record as returned
    cursor.execute("""
        UPDATE borrowed
        SET status='Returned',
            return_date=%s,
            received_by_staff_id=%s,
            pending_fines=0
        WHERE borrow_id=%s
    """, (today, receiving_staff_id, borrow_id))

    # Fnially, update book status in books list
    cursor.execute("UPDATE books SET status='Available' WHERE book_id=%s", (book_id,))

    conn.commit()
    conn.close()

    return "Book returned successfully"

