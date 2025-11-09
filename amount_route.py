# amount_route.py
from flask import Blueprint, render_template, current_app, jsonify,request
import logging

logger = logging.getLogger(__name__)

amount_bp = Blueprint('amount', __name__)

# Will be injected from app.py
Location = None
Item = None
Amount = None

@amount_bp.route('/locations', methods=['GET'])
def get_regions():
    """
    API: Returns list of unique regions for dropdown.
    """
    try:
        db = current_app.extensions['sqlalchemy']
        regions = db.session.query(Location.region).distinct().all()
        region_list = [region[0] for region in regions if region[0]]
        return jsonify(region_list), 200
    except Exception as e:
        logger.error(f"Failed to fetch regions: {e}")
        return jsonify({"error": "Failed to load regions"}), 500


@amount_bp.route('/items', methods=['GET'])
def get_items():
    """
    API: Returns all items.
    """
    try:
        db = current_app.extensions['sqlalchemy']
        all_items = Item.query.all()
        return jsonify([item.to_dict() for item in all_items]), 200
    except Exception as e:
        logger.error(f"Failed to fetch items: {e}")
        return jsonify({"error": "Failed to load items"}), 500


# --- Model injection ---


@amount_bp.route('/amount', methods=['POST'])
def amnt():
    """
    Submit amount entry.
    Required: id1, item (name), region (name), amount
    """
    try:
        id1 = request.form.get('id1')
        item_value = request.form.get('item')
        region_value = request.form.get('region')
        amount = request.form.get('amount')

        if not all([id1, item_value,region_value,amount]):
            return jsonify({'error': 'All fields required'}), 400

        # Convert
        try:
            id1 = int(id1)
            amount_val = int(amount)
        except ValueError:
            return jsonify({'error': 'id1 and amount must be integers'}), 400

        db = current_app.extensions['sqlalchemy']

        # Validate item exists
        item = Item.query.filter_by(item=item_value).first()
        if not item:
            return jsonify({'error': 'Invalid item name'}), 400

        # Validate region exists
        location = Location.query.filter_by(region=region_value).first()
        if not location:
            return jsonify({'error': 'Invalid region'}), 400

        # Create entry
        new_entry = Amount(
            id1=id1,
            item=item_value,
            region=region_value,
            amount=amount_val
        )
        db.session.add(new_entry)
        db.session.commit()

        logger.info(f"Amount submitted: {id1}, {item_value}, {region_value}, {amount_val}")

        return jsonify({
            'message': 'Amount submitted!',
            'data': new_entry.to_dict()
        }), 201

    except Exception as e:
        db = current_app.extensions['sqlalchemy']
        db.session.rollback()
        logger.exception("Amount submission failed:")
        return jsonify({'error': str(e)}), 500
    
def register_amount_model(location_model, item_model,amount_model):
    global Location, Item,Amount
    Location = location_model
    Item = item_model    
    Amount=amount_model

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
