from flask import Blueprint, request, jsonify
from ..models.feedback import Feedback
from ..database import db
import logging

feedback_bp = Blueprint('feedback', __name__)
logging.basicConfig(level=logging.INFO) 

@feedback_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        message = data.get('message')
        rating = data.get('rating')
        user_id = data.get('user_id')

        if not message or not user_id:
            return jsonify({'error': 'Message and user_id are required'}), 400

        feedback = Feedback(message=message, rating=rating, user_id=user_id)
        db.session.add(feedback)
        db.session.commit()

        return jsonify({'message': 'Feedback submitted successfully'}), 201

    except Exception as e:
        # Log error
        logging.error("Error submitting feedback: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500
