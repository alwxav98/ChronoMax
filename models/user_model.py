from db_config import db

class UserModel(db.Model):
    __tablename__ = 'Users'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    PasswordHash = db.Column(db.String(255), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, email, password_hash):
        self.Email = email
        self.PasswordHash = password_hash