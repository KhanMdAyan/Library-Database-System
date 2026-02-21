from database.connection import get_connection


def get_all_professors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professors")
    result = cursor.fetchall()
    conn.close()
    return result


def add_professor(name, department, phone, email):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO professors (name, department, phone_number, email)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (name, department, phone, email))
    conn.commit()
    conn.close()


def delete_professor(professor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM professors WHERE professor_id=%s", (professor_id,))
    conn.commit()
    conn.close()


def update_professor_fine(professor_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE professors
        SET pending_fines = pending_fines + %s
        WHERE professor_id=%s
    """, (amount, professor_id))
    conn.commit()
    conn.close()