from flask import Blueprint, request, redirect, url_for, flash, render_template,jsonify, current_app
import logging
import json
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

delete_location_bp = Blueprint('delete_location', __name__)

Location1=None

@delete_location_bp.route('/delete_location', methods=['POST'])
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
        location = Location1.query.filter_by(region=region_value).first()
        if not location:
            return jsonify({'error': 'Location not found'}), 404

        db.session.delete(location)
        db.session.commit()

        logger.info(f"Location deleted: {region_value}")

        return render_template('delete_location.html', message=f"Location '{region_value}' deleted successfully.")

    except Exception as e:
        db = current_app.extensions['sqlalchemy']
        db.session.rollback()
        logger.exception("Location deletion failed:")
        return jsonify({'error': str(e)}), 500
    
def delete_location_model(location_model):
    global Location1
    Location1 = location_model