from flask import Flask
from extensions import db, jwt
from client.routes import routes_bp

# Inicializar Flask y configuración
application = Flask(__name__)
#application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, "blacklist.db")}' # Cambiar a PostgreSQL en producción
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dmkuiAbA1fVza2ClS7jP@db-entrega1.cw1quiuqcymf.us-east-1.rds.amazonaws.com:5432/postgres'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['JWT_SECRET_KEY'] = 'supersecreto'  # Cambiar en producción

# Inicializar db y jwt
db.init_app(application)
jwt.init_app(application)

# Registrar el Blueprint para las rutas
application.register_blueprint(routes_bp)  # Registra el blueprint en la app

if __name__ == '__main__':
    application.run(host = "0.0.0.0", port = 5000, debug=True)
