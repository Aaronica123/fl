from flask import Blueprint, request, redirect, url_for, flash, render_template,jsonify, current_app
import logging
import json
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

delete_user_bp = Blueprint('delete_user1', __name__)

User=None

@delete_user_bp.route('/delete_user', methods=['POST'])
def delete_location():
    """
    Delete a location by region name.
    Required: region (name)
    """
    try:
        region_value = request.form.get('region')

        if not region_value:
            return jsonify({'error': 'Region is required'}), 400

        db = current_app.extensions['sqlalchemy']
        
        # Find and delete location
        location = User.query.filter_by(email=region_value).first()
        if not location:
            return jsonify({'error': 'Location not found'}), 404

        db.session.delete(location)
        db.session.commit()

        logger.info(f"User deleted: {region_value}")

        return render_template('delete_user.html', message=f"Location '{region_value}' deleted successfully.")

    except Exception as e:
        db = current_app.extensions['sqlalchemy']
        db.session.rollback()
        logger.exception("Location deletion failed:")
        return jsonify({'error': str(e)}), 500
    
def delete_user_model(User_model):
    global User
    User= User_model