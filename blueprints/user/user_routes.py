# user_routes.py
from flask import Blueprint, jsonify, request
from pymongo import MongoClient

user_bp = Blueprint('user', __name__)
client = MongoClient('mongodb://localhost:27017')
db = client['mydatabase']
users = db['users']

@user_bp.route('/users', methods=['GET'])
def get_users():
    all_users = list(users.find())
    return jsonify(all_users)

@user_bp.route('/users', methods=['POST'])
def add_user():
    new_user = request.json
    result = users.insert_one(new_user)
    return jsonify({"message": "User added successfully", "inserted_id": str(result.inserted_id)}), 201

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.find_one({"_id": user_id})
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    updated_user = users.update_one({"_id": user_id}, {"$set": data})
    if updated_user.modified_count > 0:
        return jsonify({"message": "User updated successfully"})
    else:
        return jsonify({"message": "User not found"}), 404

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    deleted_user = users.delete_one({"_id": user_id})
    if deleted_user.deleted_count > 0:
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"message": "User not found"}), 404
