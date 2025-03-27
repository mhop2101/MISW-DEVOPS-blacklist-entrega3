from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Inicializar Flask y configuración
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blacklist.db'  # Cambiar a PostgreSQL en producción
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecreto'  # Cambiar en producción

db = SQLAlchemy(app)
jwt = JWTManager(app)

from client.routes import *

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
