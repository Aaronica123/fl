from flask import Blueprint, render_template, current_app, jsonify,request
import logging

logger = logging.getLogger(__name__)

get_location = Blueprint('get_location', __name__)

# Will be injected from app.py
getLocation = None


@get_location.route('/api/locations', methods=['GET'])
def get_regions():
    """
    API: Returns list of unique regions for dropdown.
    """
    try:
        db = current_app.extensions['sqlalchemy']
        regions = getLocation.query.all()
        return jsonify([region.to_dict() for region in regions]), 200
    except Exception as e:
        logger.error(f"Failed to fetch regions: {e}")
        return jsonify({"error": "Failed to load regions"}), 500
    
def register_get_location_model(location_model):
    global getLocation
    getLocation = location_model