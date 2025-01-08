from db_config import db

class CronometroModel(db.Model):
    __tablename__ = 'Activities'  # Asegúrate de que coincida con el nombre de la tabla

    ID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, nullable=False)
    ActivityName = db.Column(db.String(255), nullable=False)
    Duration = db.Column(db.Integer, nullable=False)  # Cambiar a "duration" en lugar de "time_elapsed"
    ActivityDate = db.Column(db.DateTime, default=db.func.now())  # Fecha por defecto

    def __init__(self, user_id, activity_name, duration):
        self.UserID = user_id
        self.ActivityName = activity_name
        self.Duration = duration

