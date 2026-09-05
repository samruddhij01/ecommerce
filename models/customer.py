from config import get_db_connection

def get_all_customers():
    """Fetch all customers from the database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return customers


def get_customer_by_id(customer_id):
    """Fetch a single customer by their ID."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    return customer


def get_customer_by_email(email):
    """Fetch a single customer by their email (useful for checking duplicates)."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    return customer


def create_customer(name, email):
    """Insert a new customer and return their new ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, email) VALUES (%s, %s)",
        (name, email)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def update_customer(customer_id, name, email):
    """Update a customer's name and email."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET name = %s, email = %s WHERE customer_id = %s",
        (name, email, customer_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    conn.close()
    return rows_affected > 0


def delete_customer(customer_id):
    """Delete a customer by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    conn.close()
    return rows_affected > 0


def get_customer_order_history(customer_id):
    """Fetch all orders placed by a specific customer (join with orders table)."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT order_id, status, order_date, total_amount
        FROM orders
        WHERE customer_id = %s
        ORDER BY order_date DESC
        """,
        (customer_id,)
    )
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders