import json

# Local modules
import api.datamodel as dm


# CRUD APIs
def test_master_data_insert(setup_app):
    client = setup_app.test_client()
    resp = client.post("/insert_data",
                       data=json.dumps({
                           "key": "item",
                           "data": {
                               "item_name": "Apple"
                           }

                       }),
                       content_type='application/json')
    assert resp.status_code == 200
    json_data = json.loads(resp.get_data())
    instance = dm.db.session.query(dm.Item) \
        .filter_by(item_id=int(json_data['data']['id'])).one_or_none()
    dm.db.session.delete(instance)
    dm.db.session.commit()


def test_master_data_insert_empty_string(setup_app):
    client = setup_app.test_client()
    resp = client.post("/insert_data",
                       data=json.dumps({
                           "key": "store",
                           "data": {
                               "store_name": "",
                           }

                       }),
                       content_type='application/json')
    assert resp.status_code == 200
    json_data = json.loads(resp.get_data())
    instance = dm.db.session.query(dm.Store) \
        .filter_by(store_id=int(json_data['data']['id'])) \
        .one_or_none()
    dm.db.session.delete(instance)
    dm.db.session.commit()


def test_master_data_update(setup_app, fill_all_tables):
    store_id = dm.db.session.query(dm.Store) \
        .filter_by(store_name='Lifestyle') \
        .one_or_none().store_id
    sample_data = {"key": "store",
                   "key_id_value": store_id,
                   "data": {"store_name": "Lifestyle2"}}
    json_sample = json.dumps(sample_data)
    client = setup_app.test_client()
    resp = client.put("/update_data",
                      data=json_sample,
                      content_type='application/json')

    store_name = dm.db.session.query(dm.Store.store_name) \
        .filter_by(store_id=store_id) \
        .one_or_none().store_name

    assert store_name == sample_data['data']['store_name']
    assert resp.headers['X-Custom-Message'] == \
           "Record updated successfully for id: " + str(store_id)


def test_master_data_by_table(setup_app, fill_all_tables):
    client = setup_app.test_client()
    resp = client.get("http://localhost:5000/get_data_by_table"
                      "?key=item")
    assert resp.status_code == 204


def test_master_data_by_table_failure(setup_app, fill_all_tables):
    client = setup_app.test_client()
    resp = client.get("http://localhost:5000/get_data_by_table"
                      "?key=items")
    assert resp.status_code == 400


def test_master_data_delete(setup_app, fill_all_tables):
    store_id = dm.db.session.query(dm.Store) \
        .filter_by(store_name='Lifestyle') \
        .one_or_none().store_id
    client = setup_app.test_client()
    resp = client.delete("/delete_data",
                         data=json.dumps({
                             "key": "store",
                             "key_id_value": store_id
                         }),
                         content_type='application/json')
    assert resp.status_code == 200
    assert resp.headers['X-Custom-Message'] == \
           "Record deleted successfully for id: 1000000"
