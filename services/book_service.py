from database.connection import get_connection

def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    result = cursor.fetchall()
    conn.close()
    return result

def add_book(title, topics, isbn, price):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO books (book_title, book_topics, isbn, book_price)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (title, topics, isbn, price))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
    conn.commit()
    conn.close()

def search_book_by_id_or_isbn(value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM books 
        WHERE book_id=%s OR isbn=%s
    """, (value, value))
    result = cursor.fetchall()
    conn.close()
    return result