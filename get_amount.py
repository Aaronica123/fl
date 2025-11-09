from flask import Blueprint, jsonify, current_app
from sqlalchemy import func

get_amount_bp = Blueprint('get_amount', __name__)

# Global variable to hold the Amount model class
AmountModel = None


@get_amount_bp.route('/get_amount', methods=['GET'])
def get_all_amounts():
    """Fetches all records from the 'amount' table."""
    try:
        if AmountModel is None:
            return jsonify({'error': 'AmountModel not initialized for retrieval route'}), 500

        db = current_app.extensions['sqlalchemy']
        
        stmt = db.select(
            AmountModel.region,
            AmountModel.item,
            # Calculate the sum of the 'amount' column and label the result as 'total'
            func.sum(AmountModel.amount).label("total") 
        ).where(
            # 2. Filter out null regions
            AmountModel.region.isnot(None)
        ).group_by(
            # 3. Group the results by the non-aggregated columns
            AmountModel.item,
            AmountModel.region
        ).order_by(
            # 4. Order the final results
            AmountModel.region
        )
        # Query all records
        results = db.session.execute(stmt).all()

        # Format the results into a list of dictionaries (r is a Row object)
        amounts_data = [
            # Access columns by their names defined in the select statement
            {'region': r.region, 'item': r.item, 'total': r.total}
            for r in results
        ]
        return jsonify({
            'message': 'Successfully retrieved all amounts',
            'amounts': amounts_data,
            'count': len(amounts_data)
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error retrieving amounts: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# Function to inject the model
def register_get_amount_model(model_class):
    """Sets the global AmountModel class for this blueprint."""
    global AmountModel
    AmountModel = model_class