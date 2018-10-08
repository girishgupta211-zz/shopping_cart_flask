from api.datamodel.shopping_tables import (Store, Item, ShoppingList)
from api.datamodel.data_model import DataModels
from api.datamodel.data_model import db

# https://stackoverflow.com/questions/31079047/python-pep8-class-in-init-imported-but-not-used
__all__ = [Item, Store, ShoppingList, DataModels, db]

from sqlalchemy import orm

orm.configure_mappers()
