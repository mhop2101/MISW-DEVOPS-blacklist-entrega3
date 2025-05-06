from extensions import db


class Blacklist(db.Model):
    __tablename__ = 'blacklist'  # El nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    app_uuid = db.Column(db.String(36), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return f"<Blacklist {self.email}>"
