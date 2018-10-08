from api.datamodel.data_model import DataModels, db, PrimitiveAttributes


@DataModels.register_model
class Store(db.Model, PrimitiveAttributes):
    __tablename__ = 'store'
    __friendname__ = 'store'
    store_id_seq = db.Sequence(
        'store_id',
        start=1000000,
        increment=1)
    store_id = db.Column(
        db.Integer,
        store_id_seq,
        primary_key=True,
        info={'human_name': 'Store id',
              'machine_name': 'store_id',
              'display': True,
              'type': 'INT'}
    )

    store_name = db.Column(
        db.Text,
        info={'human_name': 'Store Name',
              'machine_name': 'store_name',
              'display': True,
              'type': 'TEXT'}
    )

    def __repr__(self):
        return 'store_id {}'. \
            format(self.store_id)


@DataModels.register_model
class Item(db.Model, PrimitiveAttributes):
    __tablename__ = 'item'
    __friendname__ = 'item'
    item_id_seq = db.Sequence(
        'item_id',
        start=1000000,
        increment=1)
    item_id = db.Column(
        db.Integer,
        item_id_seq,
        primary_key=True,
        info={'human_name': 'Item id',
              'machine_name': 'item_id',
              'display': True,
              'type': 'INT'}
    )

    item_name = db.Column(
        db.Text,
        info={'human_name': 'Item Name',
              'machine_name': 'item_name',
              'display': True,
              'type': 'TEXT'}
    )

    # loans = db.relationship('LoanAttributeMapping',
    #                         back_populates='attributes')

    def __repr__(self):
        return 'item id {}'. \
            format(self.item_id)


@DataModels.register_model
class ShoppingList(db.Model, PrimitiveAttributes):
    __tablename__ = 'shopping_list'
    __friendname__ = 'shopping_list'
    shopping_list_id_seq = db.Sequence(
        'shopping_list_id',
        start=1000000,
        increment=1)
    shopping_list_id = db.Column(
        db.Integer,
        shopping_list_id_seq,
        primary_key=True,
        info={'human_name': 'shopping List Id',
              'machine_name': 'shopping_list_id',
              'display': True,
              'type': 'INT'}
    )

    store_id = db.Column(
        db.Integer,
        db.ForeignKey('store.store_id'),
        info={'human_name': 'store ID',
              'machine_name': 'store_id',
              'display': False,
              'type': 'FK',
              'table_name': 'store',
              'value_col': 'store_name'}
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey('item.item_id'),
        info={'human_name': 'Item ID',
              'machine_name': 'item_id',
              'display': False,
              'type': 'FK',
              'table_name': 'store',
              'value_col': 'store_name'}
    )

    quantity = db.Column(
        db.Integer,
        info={'human_name': 'Quantity',
              'machine_name': 'quantity',
              'display': True,
              'type': 'INT'}
    )

    def __repr__(self):
        return 'shopping_list_id {}, quantity {}'. \
            format(self.shopping_list_id, self.quantity)
