import api.datamodel as dm
from api import create_app

app = create_app('config/config.yml')
with app.app_context():
    dm.db.create_all()

if __name__ == "__main__":
    app.run(threaded=True)
