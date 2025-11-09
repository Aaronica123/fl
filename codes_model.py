# location.py
from sqlalchemy import Column, Integer, Float, Text
from sqlalchemy.orm import relationship


def codes_model(Model):
    """
    Factory function that returns a Location model class.
    Model: should be db.Model from your app
    """
    class codes(Model):
        __tablename__ = 'codes'

        id1 = Column(Integer, primary_key=True)
        
        code = Column(Float, nullable=False,unique=True)

       

        def to_dict(self):
            return {
                'id1': self.id1,
                 'code': self.code
            }

        def __repr__(self):
            return f"<Location {self.code}>"

    return codes