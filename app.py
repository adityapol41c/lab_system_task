# app.py
from flask import Flask
from blueprints.user.user_routes import user_bp
from blueprints.customer.customer_routes import customer_bp
from flask_pymongo import PyMongo

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(customer_bp)

if __name__ == "__main__":
    app.run(debug=True,port=3000)
