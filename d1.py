
# class Location(db.Model):
#     __tablename__ = 'locations'
#     id = db.Column(db.Integer, primary_key=True)
#     region = db.Column(db.Text, nullable=False)
#     latitude = db.Column(db.Float, nullable=False)
#     longitude = db.Column(db.Float, nullable=False)

#     def to_dict(self):
#         return {
#             'region': self.region,
#             'latitude': self.latitude,
#             'longitude': self.longitude
#         }

# class items(db.Model):
#     __tablename__='items'
#     id = db.Column(db.Integer, primary_key=True)
#     item=db.Column(db.String(255), nullable=False)
    
#     def to_dict(self):
#         return {
#             'item':self.item
#         }

# class amount(db.Model):
#     __tablename__='amount'
#     id1=db.Column(db.Integer, primary_key=True)
#     item=db.Column(db.String(255), nullable=False)
#     amount=db.Column(db.Integer, nullable=False)
#     region=db.Column(db.String(255), nullable=False)   
    
#     def to_dict(self):
#         return {
#             'id1':self.id1,
#             'item':self.item,
#             'amount':self.amount,
#             'region':self.region
#         }
        

# @app.route('/')
# def index():
#     return render_template('users.html')

# @app.route('/api/locations')
# def api_locations():
#     locations = Location.query.all()
#     return jsonify([loc.to_dict() for loc in locations])

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
    
# @app.route('/del_location',methods=['POST'])
# def locate():
#     try:
#         region=request.form.get('region')
#         latitude=request.form.get('latitude')
#         longitude=request.form.get('longitude')
        
#         new_location=Location(
#             region=region,
#             latitude=latitude,
#             longitude=longitude
#         )
#         db.session.add(new_location)
#         db.session.commit()
        
#         return jsonify({
#             'message': 'Location added successfully',
            
#         })
        
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)})
    
        

# @app.route('/items', methods=['GET'])
# def get_items():
#     all_items = items.query.all()
#     return jsonify([item.to_dict() for item in all_items])
    
# @app.route('/items1',methods=['POST'])
# def send_items():
#     try:
#         item=request.form.get('item')
#         new_item=items(
#             item=item
#         )
#         db.session.add(new_item)
#         db.session.commit()
#         return jsonify({
#             'message': 'Item added successfully',
            
#         })
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)})
    

        
# @app.route('/api/users', methods=['POST'])
# def api_users():
#     try:
#         # 1. Get form data
#         id1=request.form.get('id1')
#         first_name = request.form.get('first_name')
#         last_name  = request.form.get('last_name')
#         email      = request.form.get('email')
#         password   = request.form.get('password')

#         # 2. Validate
#         if not all([first_name, last_name, email, password]):
#             return jsonify({'error': 'All fields are required'}), 400


#         # 3. Create user → password auto-encrypted via setter
#         new_user = user(
#             id1=id1,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             password_plain=password  # ← triggers bcrypt encryption
#         )

#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify({
#             'message': 'User created successfully',
#             'user': new_user.to_dict()
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# @app.route('/amount', methods=['POST'])
# def amnt():
#     try:
#         id1 = request.form.get('id1')
#         item_name = request.form.get('item')      # ← string
#         region = request.form.get('region')       # ← string
#         amount_val = request.form.get('amount')

#         if not all([id1, item_name, region, amount_val]):
#             return jsonify({'error': 'All fields required'}), 400

#         # Validate item exists
#         if not items.query.filter_by(item=item_name).first():
#             return jsonify({'error': 'Invalid item name'}), 400

#         # Validate region exists
#         if not Location.query.filter_by(region=region).first():
#             return jsonify({'error': 'Invalid region'}), 400

#         new_entry = amount(
#             id1=int(id1),
#             item=item_name,        # ← store string
#             amount=int(amount_val),
#             region=region
#         )
#         db.session.add(new_entry)
#         db.session.commit()

#         return jsonify({
#             'message': 'Amount submitted!',
#             'data': new_entry.to_dict()
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500
    
# if __name__ == '__main__':
#     # Create tables if they don't exist (only for dev)
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
