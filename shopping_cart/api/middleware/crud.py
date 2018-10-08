import json
import re

import api.datamodel as dm
import pandas as pd
from api.log_utils import get_logger
from flask import abort, make_response
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect


def cleanup_request_data(data):
    for key, value in data.items():
        if value == "":
            data[key] = None
    return data


def do_master_data_insert(input):
    """
    This function inserts data into any master table
    input:  dict containing
            key - friendly name corresponding to a master table
            data - to be inserted in the table
    """
    try:
        model_name = dm.DataModels.get_tablename_from_friendname(input['key'])
        data = input['data']
        data['is_active'] = True

        # Fix bug - on receiving empty string in request for any column,
        # we need to replace it with None.
        # Clean up data
        data = cleanup_request_data(data)

        model = dm.DataModels.get_model(model_name)
        data[inspect(model).primary_key[0].name] = None
        new_entry = model(**data)
        dm.db.session.add(new_entry)
        dm.db.session.commit()
        identity_column = getattr(model, inspect(model).primary_key[0].name)
        inserted_id = new_entry.query.with_entities(identity_column). \
            order_by(identity_column.desc()).first()[0]

        data = json.dumps({
            'data': {'id': inserted_id}
        })
        resp = make_response(data, 200)
        resp.headers["X-Custom-Message"] = 'Data inserted successfully'
        return resp

    except IntegrityError as e:
        get_logger().error(str(e.args[0]))
        resp = make_response("", 409)
        resp.headers["X-Custom-Message"] = \
            "Duplicate key value violets unique constraint. " \
            "Please try some different value"
        return resp
        # https://stackoverflow.com/questions/3825990/http-response-code-for-
        # poxists?ut_medium=organic
        # &utm_source=google_rich_qa&utm_campaign=google_rich_qa
        # this still needs open discussions as there are different
        # opinions for the same
    except exc.SQLAlchemyError as e:
        get_logger().error(str(e.args[0]))
        abort(400)


def do_master_data_delete(input):
    """
    This function deletes data from any master table for given id
    input:  dict containing
        key - friendly name corresponding to a master table
        key_id_value - value of primary key
    """
    try:
        model_name = dm.DataModels.get_tablename_from_friendname(input['key'])
        model = dm.DataModels.get_model(model_name)
        identity_column = getattr(model, inspect(model).primary_key[0].name)

        # First check if the entry exists or not
        column_id = input['key_id_value']
        if dm.db.session.query(model).filter(
                identity_column == column_id).first() is None:
            values = "key: {key} id value: {key_id_value}".format(**input)
            msg = "Attempt to soft-delete nonexistant value.  %s" % values
            get_logger().error(msg)
            resp = make_response("", 400)
            resp.headers["X-Custom-Message"] = msg
            return resp

        # If the id exists, soft-delete it
        dm.db.session.query(model).filter(identity_column == column_id).update(
            {'is_active': False})
        dm.db.session.commit()

        resp = make_response("", 200)
        resp.headers[
            "X-Custom-Message"] = 'Record deleted successfully for id: ' + str(
            column_id)
        return resp

    except exc.SQLAlchemyError as e:
        get_logger().error(str(e.args[0]))
        abort(400)


def do_master_data_update(input):
    """
    This function updates data into any master table for given id
        input:  dict containing
            key - friendly name corresponding to a master table
            key_id_value - value of primary key
            data : all the data to be updated in key-value format
    """
    try:
        model_name = dm.DataModels.get_tablename_from_friendname(input['key'])
        data = input['data']

        # Cleanup data
        data = cleanup_request_data(data)
        column_id = input['key_id_value']
        model = dm.DataModels.get_model(model_name)
        identity_column = getattr(model, inspect(model).primary_key[0].name)
        result = dm.db.session.query(model).filter(
            identity_column == column_id).update(data)
        dm.db.session.commit()
        if result:
            resp = make_response("", 200)
            resp.headers["X-Custom-Message"] = \
                'Record updated successfully for id: ' + str(column_id)
            return resp
        else:
            resp = make_response("", 204)
            resp.headers["X-Custom-Message"] \
                = "No record found to be updated for id: " + str(column_id)
            return resp

    except IntegrityError as e:
        get_logger().error(str(e.args[0]))
        resp = make_response("", 409)
        resp.headers["X-Custom-Message"] = \
            "Duplicate key value violets unique constraint. " \
            "Please try some different value"
        return resp
    except exc.SQLAlchemyError as e:
        get_logger().error(str(e.args[0]))
        abort(400)


def do_master_data_get_for_column(input):
    """
    This function gets data from any master table for a given column
    input:  dict containing
            key - friendly name corresponding to a master table
            key_column - column for which data is required for drop down
    """
    try:
        model_name = dm.DataModels.get_tablename_from_friendname(input['key'])
        model = dm.DataModels.get_model(model_name)
        identity_column = getattr(model, inspect(model).primary_key[0].name)
        name_column = getattr(model, input['key_column'])
    except (KeyError, TypeError):
        msg = "invalid master data get request: %s" % str(input)
        get_logger().error(msg)
        resp = make_response("", 400)
        resp.headers["X-Custom-Message"] = msg
        return resp
    table_data = dm.db.session.query(identity_column, name_column,
                                     model.is_active). \
        filter_by(is_active=True).all()
    table_data = [
        {
            'key': data[0],
            'text': data[1],
            'value': data[0],
            'is_active': data[2]
        } for data in table_data
    ]

    if len(table_data):
        resp_data = json.dumps({
            'data': table_data
        }, default=str)
        resp = make_response(resp_data, 200)
        resp.headers["X-Custom-Message"] = 'Data Fetched successfully'
        return resp
    else:
        resp = make_response("", 204)
        resp.headers["X-Custom-Message"] = 'No records found for ' \
                                           + input['key']
        return resp


def do_master_data_get_for_table(input):
    """
    This function gets data from any master table for a given column
    input:  dict containing
            key - friendly name corresponding to a master table
    """
    try:
        model_name = dm.DataModels.get_tablename_from_friendname(input)
        if model_name is None:
            msg = "%s is not registered in data models" % str(input)
            get_logger().error(msg)
            resp = make_response("", 400)
            resp.headers["X-Custom-Message"] = msg
            return resp

    except KeyError:
        msg = "Invalid request in master get for table: %s" % str(input)
        get_logger().error(msg)
        resp = make_response("", 400)
        resp.headers["X-Custom-Message"] = msg
        return resp

    table_data = []
    model = dm.DataModels.get_model(model_name)
    for row in model.query.filter_by(is_active=True).all():
        row_dict = dm.data_model.as_dict(row)
        table_data.append({**row_dict})
    df = pd.DataFrame(table_data)
    df = df.where((pd.notnull(df)), None)

    # Fixed bug - pd.NaT gets filled into an empty cell corresponding
    # to datetime columns which bothers jsonify.
    # So we replace the NaT with None, just like other columns.
    if not df.empty:
        df['update_date'] = df['update_date'].astype(object). \
            where(df.update_date.notnull(), None)
        df['create_date'] = df['create_date'].astype(object). \
            where(df.update_date.notnull(), None)
        resp_data = json.dumps({
            'data': table_data
        }, default=str)
        resp = make_response(resp_data, 200)
        resp.headers["X-Custom-Message"] = 'Data Fetched successfully'
        return resp
    else:
        resp = make_response("", 204)
        resp.headers["X-Custom-Message"] = 'No records found for ' + str(input)
        return resp


