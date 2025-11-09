
# location.py
from sqlalchemy import Column, Integer, Float, Text

def amount_model(Model):
    """
    Factory function that returns a Location model class
    Model: should be db.Model from your app
    """
    class amount(Model):
        __tablename__='amount'

        id1 = Column(Integer, primary_key=True)
        item = Column(Text, nullable=False)
        amount = Column(Float, nullable=False)
        region = Column(Text, nullable=False)

        def to_dict(self):
            return {
                'id1': self.id1,
                'item': self.item,
                'amount': self.amount,
                'region': self.region
            }

    return amount

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