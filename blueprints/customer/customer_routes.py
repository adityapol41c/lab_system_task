# customer_routes.py
from flask import Blueprint, jsonify, request
from pymongo import MongoClient

customer_bp = Blueprint('customer', __name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
customers = db['customers']

@customer_bp.route('/customers', methods=['GET'])
def get_customers():
    all_customers = list(customers.find())
    return jsonify(all_customers)

@customer_bp.route('/customers', methods=['POST'])
def add_customer():
    new_customer = request.json
    result = customers.insert_one(new_customer)
    return jsonify({"message": "Customer added successfully", "inserted_id": str(result.inserted_id)}), 201

@customer_bp.route('/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = customers.find_one({"_id": customer_id})
    if customer:
        return jsonify(customer)
    else:
        return jsonify({"message": "Customer not found"}), 404

@customer_bp.route('/customers/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json
    updated_customer = customers.update_one({"_id": customer_id}, {"$set": data})
    if updated_customer.modified_count > 0:
        return jsonify({"message": "Customer updated successfully"})
    else:
        return jsonify({"message": "Customer not found"}), 404

@customer_bp.route('/customers/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    deleted_customer = customers.delete_one({"_id": customer_id})
    if deleted_customer.deleted_count > 0:
        return jsonify({"message": "Customer deleted successfully"})
    else:
        return jsonify({"message": "Customer not found"}), 404
