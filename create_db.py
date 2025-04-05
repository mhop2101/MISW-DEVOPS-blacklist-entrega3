from application import db, application

with application.app_context():
    db.create_all()
