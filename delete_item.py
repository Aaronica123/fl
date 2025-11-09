from flask import Blueprint, request, redirect, url_for, flash, render_template,jsonify, current_app
import logging
import json
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

delete_item_bp = Blueprint('delete_item', __name__)

Item1=None

@delete_item_bp.route('/delete_item', methods=['POST'])
def delete_item():
    """
    Delete a location by region name.
    Required: region (name)
    """
    try:
        item_value = request.form.get('item')

        if not item_value:
            return jsonify({'error': 'item is required'}), 400

        db = current_app.extensions['sqlalchemy']
        
        # Find and delete location
        location = Item1.query.filter_by(item=item_value).first()
        if not location:
            return jsonify({'error': 'Location not found'}), 404

        db.session.delete(location)
        db.session.commit()

        logger.info(f"Location deleted: {item_value}")

        return render_template('delete_location.html', message=f"Location '{item_value}' deleted successfully.")

    except Exception as e:
        db = current_app.extensions['sqlalchemy']
        db.session.rollback()
        logger.exception("Location deletion failed:")
        return jsonify({'error': str(e)}), 500
    
def delete_item_model(item_model):
    global Item1
    Item1 = item_model