from flask import Blueprint, render_template, request, session, current_app, jsonify, redirect
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func # <-- NEW IMPORT

login_bp = Blueprint('login',__name__)

# Will be injected from app.py
User = None

@login_bp.route('/logout', methods=['POST'])
def logout():
    """
    Clears the server-side session variables (user_id, user_email, first_name).
    The client-side (items.html JavaScript) handles the redirection and local storage clearance.
    """
    # Remove the keys that signify an active user session
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('first_name', None)
    current_app.logger.info("Server session cleared for user.")
    return jsonify({"message": "Logout successful"}), 200
# 

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login endpoint.
    POST: JSON response (for AJAX/client-side session flow)
    GET: Render login.html
    """
    if request.method == 'GET':
        return render_template('login.html')

    # POST Logic for Authentication
    try:
        # Flask usually reads from request.form for POST, but the client is sending JSON
        data = request.get_json(silent=True)
        if not data:
            current_app.logger.warning("Login attempt failed: Invalid JSON payload received.")
            return jsonify({"error": "Invalid request format."}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            current_app.logger.warning("Login attempt failed: Missing email or password in payload.")
            return jsonify({"error": "Email and password are required"}), 400

        # Input email is lowercased for comparison
        email = email.strip().lower()

        # Retrieve database instance from the app context
        db = current_app.db

        # Find user using a robust, case-insensitive query on the email column.
        # This addresses potential case-sensitivity issues in the PostgreSQL database.
        user = db.session.query(User).filter(func.lower(User.email) == email).first()
        
        if not user:
            current_app.logger.info(f"Login failed for email: {email} - User not found in DB (Case 1).")
            # Use a generic error message for security
            return jsonify({"error": "Invalid email or password."}), 401
        
        # --- DEFENSIVE MEASURE ---
        # Ensure the user object is fresh before password verification
        db.session.rollback() 
        db.session.refresh(user)


        # Use model's secure verify_password()
        if user.verify_password(password):
            
            # --- SUCCESS PATH ---
            current_app.logger.info(f"Login SUCCESS for user: {user.email}")
            
            # 1. Declare and set server-side session variables
            session['user_id'] = user.id1
            session['user_email'] = user.email
            session['first_name'] = user.first_name

            # 2. Return JSON success message. 
            return render_template('item.html')
        else:
            # Password mismatch
            current_app.logger.info(f"Login FAILED for email: {email} - Password verification failed (Case 2).")
            return jsonify({"error": "Invalid email or password."}), 401
    
    except Exception as e:
        # Catching generic server errors (e.g., DB connection issues, broken model function)
        current_app.logger.error(f"Critical error during login POST processing.", exc_info=True)
        return jsonify({"error": "An unexpected server error occurred. Please check server logs."}), 500


# --- Model injection ---
def register_users_model(model_class):
    global User
    User = model_class