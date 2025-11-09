# from flask import Flask, jsonify, render_template,request,redirect
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.dialects.postgresql import BYTEA
# import os
# import bcrypt
# db=SQLAlchemy()

# class items(db.Model):
#     __tablename__='items'
#     id = db.Column(db.Integer, primary_key=True)
#     item=db.Column(db.String(255), nullable=False)
    
#     def to_dict(self):
#         return {
#             'item':self.item
#         }

# class codes(db.Model):
#     __tablename__='codes'
#     id = db.Column(db.Integer, primary_key=True)
#     code=db.Column(db.String(255), nullable=False)
    
#     def to_dict(self):
#         return {
#             'code':self.code
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
        

# class user(db.Model):
#     __tablename__ = 'users'
#     id1        = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(255))
#     last_name  = db.Column(db.String(255))
#     email      = db.Column(db.String(255), nullable=False, unique=True)
#     password   = db.Column(db.String(255), nullable=False)   # hex-encoded bcrypt hash

#     @property
#     def password_plain(self):
#         """Never expose the raw hash – this property is write-only."""
#         raise AttributeError("password_plain is write-only")

#     @password_plain.setter
#     def password_plain(self, plaintext: str):
#         """
#         Hash the supplied plaintext password with bcrypt and store the
#         result as a hex string in the ``password`` column.
#         """
#         if not plaintext:
#             raise ValueError("Password cannot be empty")

#         hashed_bytes = bcrypt.hashpw(plaintext.encode('utf-8'), bcrypt.gensalt())
#         self.password = hashed_bytes.hex()          # ← VARCHAR(255)

#     # -----------------------------------------------------------------
#     # Verify a candidate password
#     # -----------------------------------------------------------------
#     def verify_password(self, candidate: str) -> bool:
#         """
#         Return True if *candidate* matches the stored hash.
#         """
#         if not self.password or not candidate:
#             return False

#         try:
#             stored_hash_bytes = bytes.fromhex(self.password)   # hex → bytes
#             return bcrypt.checkpw(candidate.encode('utf-8'), stored_hash_bytes)
#         except (ValueError, TypeError):
#             return False

    # -----------------------------------------------------------------
    # Optional helper
    # -----------------------------------------------------------------
    # def to_dict(self, include_password: bool = False):
    #     data = {
    #         'id1': self.id1,
    #         'first_name': self.first_name,
    #         'last_name': self.last_name,
    #         'email': self.email,
    #     }
    #     if include_password:
    #         data['password_hash'] = self.password   # still a hex string
    #     return data