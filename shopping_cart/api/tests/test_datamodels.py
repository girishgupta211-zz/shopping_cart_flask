import api.datamodel as dm


def test_get_db_connection(setup_app):
    assert dm.db.get_engine()


def test_data_model_registration(setup_app):
    expected_registered_models = ['shopping_list', 'item', 'store']
    actual_registered_models = list(dm.DataModels.models.keys())
    print(set(actual_registered_models) - set(expected_registered_models))
    assert all(x in expected_registered_models
               for x in actual_registered_models)
