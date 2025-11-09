
from sqlalchemy import Column, Integer, Float, Text

def main_item(Model):
    """
    Factory function that returns a Location model class
    Model: should be db.Model from your app
    """
    class item(Model):
        __tablename__='items'

        id = Column(Integer, primary_key=True)
        item = Column(Text, nullable=False)
       

        def to_dict(self):
            return {
                'item':self.item
            }

    return item


#     id = db.Column(db.Integer, primary_key=True)
#     item=db.Column(db.String(255), nullable=False)
    
#     def to_dict(self):
#         return {
#             'item':self.item
#         }