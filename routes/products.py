from flask import Blueprint, request, jsonify
from models.product import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product_stock,
    delete_product
)

products_bp = Blueprint('products', __name__)


@products_bp.route('/products', methods=['GET'])
def list_products():
    """GET /products - returns all products"""
    products = get_all_products()
    return jsonify(products), 200


@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """GET /products/5 - returns one product by ID"""
    product = get_product_by_id(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


@products_bp.route('/products', methods=['POST'])
def add_product():
    """POST /products - creates a new product"""
    data = request.json

    required_fields = ['name', 'price', 'stock', 'category_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    new_id = create_product(data['name'], data['price'], data['stock'], data['category_id'])
    return jsonify({"message": "Product created", "product_id": new_id}), 201


@products_bp.route('/products/<int:product_id>/stock', methods=['PUT'])
def update_stock(product_id):
    """PUT /products/5/stock - updates stock for a product"""
    data = request.json
    if 'stock' not in data:
        return jsonify({"error": "Missing field: stock"}), 400

    success = update_product_stock(product_id, data['stock'])
    if not success:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"message": "Stock updated"}), 200


@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    """DELETE /products/5 - deletes a product"""
    success = delete_product(product_id)
    if not success:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"message": "Product deleted"}), 200