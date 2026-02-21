# Student list window UI's backend working.
# fetches details, adds, removes and edits the list, updates the fine


from database.connection import get_connection


def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    result = cursor.fetchall()
    conn.close()
    return result


def add_student(name, department, class_name, phone, email):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO students (name, department, class, phone_number, email)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, department, class_name, phone, email))
    conn.commit()
    conn.close()


def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
    conn.commit()
    conn.close()


def update_student_fine(student_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students
        SET pending_fines = pending_fines + %s
        WHERE student_id=%s
    """, (amount, student_id))
    conn.commit()
    conn.close()