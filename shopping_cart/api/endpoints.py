# Local imports
from flask import Blueprint, jsonify, request

from api.middleware import crud

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    return 'This is the shopping app, please refers \
    to the documentation for usage'


hello_world_bp = Blueprint('hello_world', __name__)


@hello_world_bp.route("/hello")
def hello_world():
    return jsonify({"text": "api server says hello world"})


# CRUD Related Endpoints
master_data_insert_bp = Blueprint('master_data_insert', __name__)


@master_data_insert_bp.route('/insert_data', methods=['POST'])
def master_data_insert():
    """
    This API inserts data into master table depending upon request.
    """
    input_dict = request.get_json()
    return crud.do_master_data_insert(input_dict)


master_data_delete_bp = Blueprint('master_data_delete', __name__)


@master_data_delete_bp.route('/delete_data', methods=['DELETE'])
def master_data_delete():
    """
    This API deletes data from any master table depending upon request.
    """
    input_dict = request.get_json()
    return crud.do_master_data_delete(input_dict)


master_data_update_bp = Blueprint('master_data_update', __name__)


@master_data_update_bp.route('/update_data', methods=['PUT'])
def master_data_update():
    """
    This API updates data into master table depending upon request.
    """
    input_dict = request.get_json()
    return crud.do_master_data_update(input_dict)


master_data_get_for_column_bp = Blueprint('get_data_by_column', __name__)


@master_data_get_for_column_bp.route('/get_data_by_column')
def master_data_get():
    """
    This API gets data from a master table depending upon column request.
    """
    input_dict = {}
    input_dict['key'] = request.args.get('key')
    input_dict['key_column'] = request.args.get('key_column')

    return crud.do_master_data_get_for_column(input_dict)


master_data_get_for_table_bp = Blueprint('get_data_by_table', __name__)


@master_data_get_for_table_bp.route('/get_data_by_table')
def master_data_get_by_table():
    """
    This API fetches data from master table depending upon table.
    """
    return crud.do_master_data_get_for_table(request.args.get('key'))
