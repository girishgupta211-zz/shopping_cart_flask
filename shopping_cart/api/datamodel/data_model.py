from flask import jsonify  # this already handles datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


def as_dict(self):
    res_dict = {}
    full_dict = self.__dict__
    for attr in full_dict:
        try:
            jsonify(full_dict[attr])
        except TypeError:
            continue
        res_dict[attr] = full_dict[attr]
    return res_dict


class DataModels():
    models = {}

    @classmethod
    def add_model(cls, model):
        if model.__tablename__ not in cls.models.keys():
            cls.models[model.__tablename__] = model

    @classmethod
    def get_model(cls, model):
        try:
            return cls.models[model]
        except KeyError as e:
            print("Key {} not registered in DataModels!".format(model))
            raise (e)

    @classmethod
    def get_tablename_from_friendname(cls, friend_name):
        try:
            for key, value in cls.models.items():
                if value.__friendname__ == friend_name:
                    return key
        except KeyError as e:
            print("Input friend name not matches with any of existing models.")
            raise (e)

    @staticmethod
    def register_model(model):
        """Use this method as a decorator to register data models
         with the DataModels class and set them up with versioning"""
        DataModels.add_model(model)
        return model


class PrimitiveAttributes():
    __versioned__ = {}

    is_active = db.Column(
        db.Boolean,
        info={'human_name': 'Is Active',
              'machine_name': 'is_active',
              'display': False,
              'type': 'BOOL'}
    )
    create_date = db.Column(
        db.DateTime,
        server_default=func.now(),
        info={'human_name': 'Creation date',
              'machine_name': 'create_date',
              'display': True,
              'type': 'DATETIME'}
    )
    update_date = db.Column(
        db.DateTime,
        onupdate=func.now(),
        info={'human_name': 'Updated date',
              'machine_name': 'update_date',
              'display': True,
              'type': 'DATETIME'}
    )
    created_by = db.Column(
        db.Text,
        info={'human_name': 'Created By',
              'machine_name': 'created_by',
              'display': True,
              'type': 'TEXT'}
    )
    updated_by = db.Column(
        db.Text,
        info={'human_name': 'Updated By',
              'machine_name': 'updated_by',
              'display': True,
              'type': 'TEXT'}
    )


if __name__ == '__main__':
    from api import create_app

    app = create_app('config/config.yml')
    with app.app_context():
        db.create_all(app=app)
