from flask import Blueprint, jsonify
import logging

main_bp = Blueprint('main', __name__)

logging.basicConfig(level=logging.INFO)

@main_bp.route('/', methods=['GET'])
def home():
    try:
        return jsonify({"message": "InfinityStyleVerse backend is working!"})
    except Exception as e:
        logging.error(f"Error in home route: {e}")
        return jsonify({"message": "Internal server error"}), 500
