from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.orm.exc import NoResultFound

user_details_bp = Blueprint('user_details', __name__)

# Global variable to hold the User model class
User = None

@user_details_bp.route('/get_user_details', methods=['GET'])
def get_user_details():
    """
    Fetches detailed user information based on the email provided in the query parameters.
    This route is called after a successful login POST to quickly load session data.
    """
    email = request.args.get('email')

    if not email:
        return jsonify({'error': 'Email query parameter is required.'}), 400

    if User is None:
        return jsonify({'error': 'User model not initialized in get_user_route.py'}), 500

    try:
        # Use a database session to find the user by email
        # .one() raises NoResultFound if not found, simplifying error handling
        user_record = current_app.db.session.query(User).filter_by(email=email).one()

        # Assuming the User model has a to_dict() method which EXCLUDES the password
        return jsonify({
            'message': 'User details fetched successfully.',
            'user': user_record.to_dict()
        }), 200

    except NoResultFound:
        # User was authenticated but their details are missing or wrong in the DB
        return jsonify({'error': 'User record not found in the database.'}), 404
    
    except Exception as e:
        current_app.logger.error(f"Error fetching user details for {email}: {e}", exc_info=True)
        return jsonify({'error': f'Server error fetching details: {str(e)}'}), 500


@user_details_bp.route('/get_user_credentials', methods=['GET'])
def get_user_credentials():
    """
    NEW ROUTE: Fetches user credentials (all details EXCEPT password) based on 
    the email provided in the query parameters.
    """
    email = request.args.get('email')

    if not email:
        return jsonify({'error': 'Email query parameter is required.'}), 400

    if User is None:
        return jsonify({'error': 'User model not initialized in get_user_route.py'}), 500

    try:
        # Use a database session to find the user by email
        user_record = current_app.db.session.query(User).filter_by(email=email).one()

        # Assuming the User model's to_dict() method correctly excludes the password hash
        return jsonify({
            'message': 'User credentials fetched successfully.',
            'credentials': user_record.to_dict()
        }), 200

    except NoResultFound:
        return jsonify({'error': 'User record not found in the database for the provided email.'}), 404
    
    except Exception as e:
        current_app.logger.error(f"Error fetching user credentials for {email}: {e}", exc_info=True)
        return jsonify({'error': f'Server error fetching credentials: {str(e)}'}), 500


def register_user_details_model(model_class):
    """Sets the global User model class for this blueprint."""
    global User
    User = model_class