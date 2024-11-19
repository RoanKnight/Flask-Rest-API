from flask import Blueprint, request, jsonify
from app import db
from app.models import UserRole, Customer
from app.schemas.customer_schema import CustomerSchema
from app.middleware import token_required, role_required

customer_routes = Blueprint('customer_routes', __name__)
customer_schema = CustomerSchema()

@customer_routes.route('/customers', methods=['GET'])
@token_required
@role_required(UserRole.DIRECTOR)
def index(current_user):
  customers = Customer.query.all()
  customers_data = customer_schema.dump(customers)
  response = {
      "success": {
          "customers": customers_data
      }
  }
  return jsonify(response), 200

@customer_routes.route('/customers/<int:id>', methods=['GET'])
@token_required
@role_required(UserRole.DIRECTOR)
def show(current_user, id):
  customer = Customer.query.get(id)
  if not customer:
    return jsonify({"message": "Customer not found"}), 404

  customer_data = customer_schema.dump(customer)
  response = {
      "success": {
          "customer": customer_data
      }
  }
  return jsonify(response), 200
