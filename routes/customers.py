from flask import Blueprint, request, jsonify
from models.customer import (
    get_all_customers,
    get_customer_by_id,
    get_customer_by_email,
    create_customer,
    update_customer,
    delete_customer,
    get_customer_order_history
)

customers_bp = Blueprint('customers', __name__)


@customers_bp.route('/customers', methods=['GET'])
def list_customers():
    """GET /customers - returns all customers"""
    customers = get_all_customers()
    return jsonify(customers), 200


@customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """GET /customers/3 - returns one customer by ID"""
    customer = get_customer_by_id(customer_id)
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer), 200


@customers_bp.route('/customers', methods=['POST'])
def add_customer():
    """POST /customers - creates a new customer"""
    data = request.json

    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    existing = get_customer_by_email(data['email'])
    if existing:
        return jsonify({"error": "A customer with this email already exists"}), 409

    new_id = create_customer(data['name'], data['email'])
    return jsonify({"message": "Customer created", "customer_id": new_id}), 201


@customers_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def edit_customer(customer_id):
    """PUT /customers/3 - updates a customer's name/email"""
    data = request.json

    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    success = update_customer(customer_id, data['name'], data['email'])
    if not success:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify({"message": "Customer updated"}), 200


@customers_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def remove_customer(customer_id):
    """DELETE /customers/3 - deletes a customer"""
    success = delete_customer(customer_id)
    if not success:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify({"message": "Customer deleted"}), 200


@customers_bp.route('/customers/<int:customer_id>/orders', methods=['GET'])
def customer_orders(customer_id):
    """GET /customers/3/orders - returns a customer's order history"""
    customer = get_customer_by_id(customer_id)
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404

    orders = get_customer_order_history(customer_id)
    return jsonify(orders), 200