# library staff list window UI's backend working.
# fetches details, adds, removes and edits the list


from database.connection import get_connection


def get_all_staff():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM library_staff")
    result = cursor.fetchall()
    conn.close()
    return result


def add_staff(name, phone, email):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO library_staff (name, phone_number, email)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (name, phone, email))
    conn.commit()
    conn.close()


def delete_staff(employee_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM library_staff WHERE employee_id=%s", (employee_id,))
    conn.commit()
    conn.close()