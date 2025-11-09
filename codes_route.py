from flask import Blueprint, request, jsonify, current_app, url_for, render_template, session, redirect
from sqlalchemy.orm.exc import NoResultFound 
from sqlalchemy.exc import SQLAlchemyError

# Define the blueprint
codes_bp = Blueprint('codes_bp', __name__)

# Global variable to hold the SQLAlchemy Model (to be registered by app.py)
CodeModel = None


# --- Model Registration ---

def register_code_model(model):
    """
    Registers the Code SQLAlchemy model with this blueprint.
    This function should be called during application setup (e.g., in app.py).
    """
    global CodeModel
    CodeModel = model
    if current_app:
        if current_app.has_app_context():
            current_app.logger.info("CodeModel registered successfully for codes_bp.")


# --- Routes ---

# 1. Route to serve the items1.html file (The Dashboard)
@codes_bp.route('/prev_user')
def items1_html_route():
    """
    Renders and serves the items1.html template.
    This is often used as the target for the dashboard, 
    but for proper protection, the /home route (in app.py) is preferred.
    """
    # Check for session protection (optional, but good practice)
    if 'user_id' not in session:
        return redirect(url_for('dashboard_home')) # Redirect to code entry page
        
    return render_template('admin_dashboard.html')


# 2. API route to check the code
@codes_bp.route('/check_code', methods=['POST'])
def check_code():
    """
    API: Receives input code, checks for a match, and returns a JSON response.
    If the code matches, it sets a session flag and returns the URL for /home.
    """
    # 1. Configuration Check
    if not CodeModel:
        if current_app.has_app_context():
            current_app.logger.error("Configuration error: CodeModel is not registered.")
        return jsonify({"error": "Configuration error: Code model missing"}), 500

    # 2. Get the JSON data and validate/convert input
    try:
        data = request.get_json(silent=True)
        
        if not data or 'input_code' not in data:
            current_app.logger.warning("Code check attempt failed: Missing 'input_code' in JSON payload.")
            return jsonify({"error": "Missing 'input_code' in JSON payload"}), 400
            
        raw_input = data['input_code']
        
        try:
            # Convert input to float to match the database column type (assuming codes_model uses Float)
            input_code = float(raw_input)
        except (ValueError, TypeError):
            current_app.logger.warning(f"Code check attempt failed: Input '{raw_input}' is not a valid numeric code.")
            return jsonify({"error": "'input_code' must be a valid numeric value."}), 400
        
    except Exception:
        current_app.logger.error("Failed to process JSON request during code check.", exc_info=True)
        return jsonify({"error": "Invalid JSON request format."}), 400

    # 3. Database operation and Comparison
    try:
        db = current_app.db 
        
        # Query the database for a matching code
        code_record = db.session.query(CodeModel).filter_by(code=input_code).first()
        
        if code_record:
            current_app.logger.info(f"Code verification SUCCESS for input: {input_code}. Setting session flag.")
            
            # CRITICAL: Set the session flag to authenticate the user for subsequent requests
            session['user_id'] = 'admin_session_id' 
            
            # Redirect to the protected dashboard home page defined in app.py
            redirect_target = url_for('dashboard_home') # 'dashboard_home' is the function name for the /home route

            # Return JSON with the redirect URL for client-side navigation
            return jsonify({
                "match": True,
                "message": "Code verification successful. Redirecting...",
                "redirect_url": redirect_target
            }), 200
        else:
            current_app.logger.info(f"Code verification FAILED. Input: {input_code}, no matching record found.")
            return jsonify({
                "match": False,
                "message": "The submitted code does not match any stored code."
            }), 200

    except SQLAlchemyError as e:
        # Explicitly handle database errors
        try:
            db.session.rollback()
        except Exception:
            pass 
        current_app.logger.error("SQLAlchemy database error during code check.", exc_info=True)
        return jsonify({"error": f"Database error: {str(e)}"}), 500
        
    except Exception:
        # Catch any other unexpected server issues
        try:
            db.session.rollback()
        except Exception:
            pass 
        
        current_app.logger.error("Critical internal server error during code check.", exc_info=True)
        return jsonify({"error": "An unexpected server error occurred."}), 500