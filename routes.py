from flask import Blueprint, request, jsonify, current_app

location_bp = Blueprint('location', __name__)

# Global variable to hold the model class
Location = None


@location_bp.route('/del_location12', methods=['POST'])
def add_location():
    try:
        # Check for JSON body first, then fallback to form data
        data = request.get_json(silent=True)
        if data:
            region = data.get('region')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
        else:
            region = request.form.get('region')
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')

        if not all([region, latitude, longitude]):
            return jsonify({'error': 'region, latitude, and longitude are required'}), 400

        # Retrieve database instance from the app context
        db = current_app.extensions['sqlalchemy']

        if Location is None:
            # This error check will now pass because we fix the registration in app.py
            return jsonify({'error': 'Location model not initialized in routes.py'}), 500

        try:
            # Handle string conversion robustly
            lat = float(latitude)
            lon = float(longitude)
        except (TypeError, ValueError):
            return jsonify({'error': 'latitude and longitude must be valid numbers'}), 400

        # Create new location
        new_location = Location(
            region=region,
            latitude=lat,
            longitude=lon
        )
        db.session.add(new_location)
        db.session.commit()

        return jsonify({
            'message': 'Location added successfully',
            'location': new_location.to_dict()
        }), 201

    except Exception as e:
        # Ensure rollback in case of an error
        try:
            current_app.db.session.rollback()
        except:
            pass 
            
        current_app.logger.error(f"Error adding location: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# Function to inject the model: RENAMED FOR UNIQUE IMPORT IN app.py
def register_location_model(model_class):
    """Sets the global Location model class for this blueprint."""
    global Location
    Location = model_class