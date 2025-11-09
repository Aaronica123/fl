# routes.py
from flask import Blueprint, request, jsonify, current_app

main_item = Blueprint('main', __name__)

# Global variable to hold the model
Main = None

@main_item.route('/items1', methods=['POST'])
def item():
    try:
        item = request.form.get('item')

        if not all([item]):
            return jsonify({'error': 'item are required'}), 400

        # Get db from current_app
        db = current_app.extensions['sqlalchemy']

        new_location = Main(
            item=item
            
        )
        db.session.add(new_location)
        db.session.commit()

        return jsonify({
            'message': 'item added successfully',
            'location': new_location.to_dict()
        }), 201

    except ValueError as ve:
        db = current_app.extensions['sqlalchemy']  # Re-get in case of error
        db.session.rollback()
        return jsonify({'error': f'Invalid number: {str(ve)}'}), 400
    except Exception as e:
        db = current_app.extensions['sqlalchemy']
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Function to inject the model
def register_item_model(model_class):
    global Main
    Main = model_class