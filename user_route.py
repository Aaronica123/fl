from flask import Blueprint, request, jsonify, current_app
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)

# Will be injected from app.py
User = None


@user_bp.route('/api/users', methods=['POST'])
def register_user():
    """
    Register a new user.
    Required: first_name, last_name, email, password
    """
    try:
        # Use request.get_json() if submitted via AJAX with application/json
        # If it's a standard form submission, request.form is correct.
        data = request.form
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        if not all([first_name, last_name, email, password]):
            return jsonify({'error': 'All fields are required'}), 400

        email = email.strip().lower()
        first_name = first_name.strip()
        last_name = last_name.strip()

        db = current_app.extensions['sqlalchemy']

        # Check duplicate email
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409

        # Create user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        new_user.password_plain = password  # ← Triggers bcrypt hashing

        db.session.add(new_user)
        db.session.commit()

        logger.info(f"User registered: {email} (ID: {new_user.id1})")

        # --- MODIFIED RESPONSE: Simplified JSON success object ---
        # The client-side JavaScript should read this and handle the display/redirection.
        return jsonify({
            'message': 'User registered successfully. Redirecting to login...',
            'success': True
        }), 201

    except Exception as e:
        db = current_app.extensions['sqlalchemy']
        db.session.rollback()
        logger.exception("Registration failed:")
        return jsonify({'error': 'Registration failed. Please try again.'}), 500


# --- Inject model ---
def register_user_model(model_class):
    global User
    User = model_class