# amount_route.py
from flask import Blueprint, render_template, current_app, jsonify,request
import logging

logger = logging.getLogger(__name__)

email_bp = Blueprint('email_1', __name__)

# Will be injected from app.py
Email1 = None


@email_bp.route('/get_email', methods=['GET'])
def get_regions():
    """
    API: Returns list of unique email for dropdown.
    """
    try:
        db = current_app.extensions['sqlalchemy']
        regions = db.session.query(Email1.email).distinct().all()
        region_list = [email[0] for email in regions if email[0]]
        return jsonify(region_list), 200
    except Exception as e:
        logger.error(f"Failed to fetch regions: {e}")
        return jsonify({"error": "Failed to load regions"}), 500


    
def register_email_model(User_model):
    global Email1
    Email1 = User_model
# @app.route('/items', methods=['GET'])
# def get_items():
#     all_items = items.query.all()
#     return jsonify([item.to_dict() for item in all_items])

# @app.route('/locations', methods=['GET'])
# def locations_page():
#     try:
#         # Fetch only the 'region' field from all locations
#         regions = Location.query.with_entities(Location.region).distinct().all()
        
#         # Convert to list of strings: [('North',), ('South',)] → ['North', 'South']
#         region_list = [region[0] for region in regions]
        
#         return jsonify(region_list), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
