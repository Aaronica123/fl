# # from flask import Flask, jsonify, render_template,request,redirect
# # from flask_sqlalchemy import SQLAlchemy
# # from sqlalchemy.dialects.postgresql import BYTEA
# # import os
# # import bcrypt

# # db = SQLAlchemy()


# # class Location(db.Model):
# #     __tablename__ = 'locations'
# #     id = db.Column(db.Integer, primary_key=True)
# #     region = db.Column(db.Text, nullable=False)
# #     latitude = db.Column(db.Float, nullable=False)
# #     longitude = db.Column(db.Float, nullable=False)

# #     def to_dict(self):
# #         return {
# #             'region': self.region,
# #             'latitude': self.latitude,
# #             'longitude': self.longitude
# #         }
# # class user(db.Model):
# #     __tablename__ = 'users'
# #     id1 = db.Column(db.Integer, primary_key=True)
# #     first_name = db.Column(db.String(255), nullable=False)
# #     last_name = db.Column(db.String(255), nullable=False)
# #     email = db.Column(db.String(255), nullable=False)
# #     password=db.Column(BYTEA, nullable=False)
    
# #     @property
# #     def password_plain(self):
# #         """Never expose the raw hash – this property is write-only."""
# #         raise AttributeError("password_plain is write-only")
    
# #     @password_plain.setter
# #     def password_plain(self, plaintext: str):
# #         """
# #         Convert a normal string password into a bcrypt hash and store it
# #         in the ``password`` column (BYTEA).
# #         """
# #         # bcrypt needs bytes → encode the string
# #         salt = bcrypt.gensalt()                     # random salt each call
# #         hashed = bcrypt.hashpw(plaintext.encode('utf-8'), salt)
# #         self.password = hashed
        
# #     def verify_password(self, candidate: str) -> bool:
# #         """
# #         Return True if *candidate* matches the stored hash.
# #         """
# #         return bcrypt.checkpw(candidate.encode('utf-8'), self.password)

# #     def to_dict(self, include_password=False):
# #         data = {
# #             'id1': self.id1,
# #             'first_name': self.first_name,
# #             'last_name': self.last_name,
# #             'email': self.email,
# #         }
# #         if include_password:
# #             data['password_hash'] = self.password.hex()
# #         return data


#     if request.method == 'GET':
#         return render_template('login.html')

#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         if not email or not password:
#             return render_template('login.html', error="Both fields are required")

#         # Fetch user by email
#         user_obj = user.query.filter_by(email=email).first()

#         if not user_obj:
#             return jsonify("Invalid email or password")

#         # Verify password using bcrypt
#         if user_obj.verify_password(password):
#             # Success! You can add session/login here later
#             return render_template('item.html', success="Login successful!")

#         else:
#             return render_template('users.html', error="Invalid email or password")


