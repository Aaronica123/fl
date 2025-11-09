# user_model.py
from sqlalchemy import Column, Integer, String
import bcrypt

def create_user_model(Model):
    """
    Factory function → returns a User model matching the `users1` table.
    """
    class User(Model):
        __tablename__ = 'users1'  # ← Matches your table name

        id1 = Column(Integer, primary_key=True)
        first_name = Column(String(255), nullable=False)
        last_name = Column(String(255), nullable=False)
        email = Column(String(255), nullable=False, unique=True)
        pass_ = Column('pass', String(255), nullable=False)  # ← Maps to `pass` column

        # ------------------------------------------------------------------
        # Write-only password property
        # ------------------------------------------------------------------
        @property
        def password_plain(self):
            raise AttributeError("Password is write-only")

        @password_plain.setter
        def password_plain(self, plaintext: str):
            if not plaintext or not plaintext.strip():
                raise ValueError("Password cannot be empty")
            hashed = bcrypt.hashpw(plaintext.encode('utf-8'), bcrypt.gensalt())
            self.pass_ = hashed.hex()  # Store as hex string

        # ------------------------------------------------------------------
        # Verify password
        # ------------------------------------------------------------------
        def verify_password(self, candidate: str) -> bool:
            if not candidate:
                return False
            try:
                stored_hex = self.pass_.strip()
                stored_bytes = bytes.fromhex(stored_hex)
                return bcrypt.checkpw(candidate.encode('utf-8'), stored_bytes)
            except Exception:
                return False

        # ------------------------------------------------------------------
        # Safe to_dict()
        # ------------------------------------------------------------------
        def to_dict(self):
            return {
                'id1': self.id1,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email
            }

    return User