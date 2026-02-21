# This will send a mail to the registered mail id about the book that is overdue, once a day.
# Have to set email id and password in config, I changed it to default.

import smtplib
from email.message import EmailMessage
from datetime import date
from database.connection import get_connection
from config import EMAIL_CONFIG


def send_overdue_emails():
    conn = get_connection()
    cursor = conn.cursor()

    today = date.today()

    cursor.execute("""
        SELECT borrow_id, book_name, pending_fines,
               issued_to_id, issued_to_type,
               last_email_sent_date
        FROM borrowed
        WHERE status='Borrowed'
          AND due_date < %s
          AND (last_email_sent_date IS NULL
               OR last_email_sent_date < %s)
    """, (today, today))

    records = cursor.fetchall()

    if not records:
        conn.close()
        return "No emails to send"

    server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
    server.starttls()
    server.login(
        EMAIL_CONFIG["sender_email"],
        EMAIL_CONFIG["sender_password"]
    )

    for record in records:
        borrow_id, book_name, fine, borrower_id, borrower_type, _ = record

        # Get borrower email from db
        if borrower_type == "Student":
            cursor.execute("SELECT email FROM students WHERE student_id=%s", (borrower_id,))
        else:
            cursor.execute("SELECT email FROM professors WHERE professor_id=%s", (borrower_id,))

        result = cursor.fetchone()
        if not result:
            continue

        recipient_email = result[0]

        msg = EmailMessage()
        msg["Subject"] = "Library Overdue Reminder"
        msg["From"] = EMAIL_CONFIG["sender_email"]
        msg["To"] = recipient_email

        msg.set_content(f"""
Dear User,

This is a reminder that the following book is overdue. Not returnig it on time will result in fines.

Book Name: {book_name}
Current Pending Fine: {fine}

Please return the book as soon as possible.

Library Management System
""")

        server.send_message(msg)

        # Update last_email_sent_date to not send double emails
        cursor.execute("""
            UPDATE borrowed
            SET last_email_sent_date=%s
            WHERE borrow_id=%s
        """, (today, borrow_id))

    conn.commit()
    conn.close()
    server.quit()

    return "Overdue emails sent"