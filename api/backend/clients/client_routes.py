from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

client_routes = Blueprint('client_routes', __name__)