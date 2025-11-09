# location.py
from sqlalchemy import Column, Integer, Float, Text
from sqlalchemy.orm import relationship


def locationmodel(Model):
    """
    Factory function that returns a Location model class.
    Model: should be db.Model from your app
    """
    class Location(Model):
        __tablename__ = 'locations'

        id = Column(Integer, primary_key=True)
        region = Column(Text, nullable=False, unique=True)  # recommended: unique
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)

       

        def to_dict(self):
            return {
                'id': self.id,
                'region': self.region,
                'latitude': self.latitude,
                'longitude': self.longitude
            }

        def __repr__(self):
            return f"<Location {self.region}>"

    return Location