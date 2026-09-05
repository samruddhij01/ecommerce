from flask import Blueprint, jsonify
from config import get_db_connection

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/analytics/top-products', methods=['GET'])
def top_products():
    """
    GET /analytics/top-products
    Returns products ranked by total quantity sold, using RANK() window function.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            p.product_id,
            p.name,
            SUM(oi.quantity) AS total_sold,
            RANK() OVER (ORDER BY SUM(oi.quantity) DESC) AS sales_rank
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.name
        ORDER BY sales_rank
        LIMIT 10
    """
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(results), 200


@analytics_bp.route('/analytics/monthly-revenue', methods=['GET'])
def monthly_revenue():
    """
    GET /analytics/monthly-revenue
    Returns total revenue per month, plus a running cumulative total
    using SUM() OVER (window function).
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            DATE_FORMAT(order_date, '%Y-%m') AS month,
            SUM(total_amount) AS monthly_total,
            SUM(SUM(total_amount)) OVER (ORDER BY DATE_FORMAT(order_date, '%Y-%m')) AS running_total
        FROM orders
        GROUP BY DATE_FORMAT(order_date, '%Y-%m')
        ORDER BY month
    """
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(results), 200


@analytics_bp.route('/analytics/top-customers', methods=['GET'])
def top_customers():
    """
    GET /analytics/top-customers
    Returns customers ranked by total amount spent, using ROW_NUMBER().
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            c.customer_id,
            c.name,
            SUM(o.total_amount) AS total_spent,
            ROW_NUMBER() OVER (ORDER BY SUM(o.total_amount) DESC) AS spend_rank
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.name
        ORDER BY spend_rank
        LIMIT 10
    """
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(results), 200