from flask import Flask
from extensions import db, jwt
from client.routes import routes_bp  
import os

# Inicializar Flask y configuración
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, "blacklist.db")}' # Cambiar a PostgreSQL en producción
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dmkuiAbA1fVza2ClS7jP@db-entrega1.cw1quiuqcymf.us-east-1.rds.amazonaws.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecreto'  # Cambiar en producción

# Inicializar db y jwt
db.init_app(app)
jwt.init_app(app)

# Registrar el Blueprint para las rutas
app.register_blueprint(routes_bp)  # Registra el blueprint en la app

if __name__ == '__main__':
    app.run(debug=True)
