# routes/orders.py
from flask import Blueprint, request, jsonify
from models.order import create_order

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['POST'])
def place_order():
    data = request.json
    result = create_order(data['customer_id'], data['items'])
    return jsonify(result), 201