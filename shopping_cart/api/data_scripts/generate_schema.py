from api.datamodel import db

if __name__ == "__main__":
    from api import create_app

    app = create_app("config/config.yml")

    with app.app_context():
        db.reflect()
        db.drop_all()
        db.create_all()
