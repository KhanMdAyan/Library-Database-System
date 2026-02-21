from datetime import date
from database.connection import get_connection
from services.student_service import update_student_fine
from services.professor_service import update_professor_fine


def run_daily_fine_update():
    conn = get_connection()
    cursor = conn.cursor()

    today = date.today()

    # Get all overdue borrowed records
    cursor.execute("""
        SELECT borrow_id, book_id, issued_to_id,
               issued_to_type, due_date,
               last_fine_update_date
        FROM borrowed
        WHERE status='Borrowed'
          AND due_date < %s
          AND (last_fine_update_date IS NULL
               OR last_fine_update_date < %s)
    """, (today, today))

    records = cursor.fetchall()

    for record in records:
        borrow_id, book_id, borrower_id, borrower_type, due_date, last_update = record

        # Get book price
        cursor.execute("SELECT book_price FROM books WHERE book_id=%s", (book_id,))
        price = cursor.fetchone()[0]

        # Determine daily fine
        if borrower_type == "Student":
            daily_fine = price * 0.02
            update_student_fine(borrower_id, daily_fine)
        else:
            daily_fine = price * 0.05
            update_professor_fine(borrower_id, daily_fine)

        # Update borrowed table
        cursor.execute("""
            UPDATE borrowed
            SET pending_fines = pending_fines + %s,
                last_fine_update_date = %s
            WHERE borrow_id=%s
        """, (daily_fine, today, borrow_id))

    conn.commit()
    conn.close()

    return "Daily fine update completed"