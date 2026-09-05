# models/order.py
from config import get_db_connection

def create_order(customer_id, items):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO orders (customer_id) VALUES (%s)", (customer_id,)
        )
        order_id = cursor.lastrowid

        total = 0
        for item in items:
            cursor.execute("SELECT price, stock FROM products WHERE product_id=%s", (item['product_id'],))
            price, stock = cursor.fetchone()
            if stock < item['quantity']:
                raise Exception("Insufficient stock")

            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (%s,%s,%s,%s)",
                (order_id, item['product_id'], item['quantity'], price)
            )
            cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE product_id=%s",
                (item['quantity'], item['product_id'])
            )
            total += price * item['quantity']

        cursor.execute("UPDATE orders SET total_amount=%s WHERE order_id=%s", (total, order_id))
        conn.commit()   # all-or-nothing: transaction success
        return {"order_id": order_id, "total": float(total)}
    except Exception as e:
        conn.rollback()  # undo everything if anything failed
        raise e
    finally:
        cursor.close()
        conn.close()