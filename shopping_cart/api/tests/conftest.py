import tempfile

import pytest

import api.datamodel as dm
from api import create_app
from api.log_utils import logger


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


@static_vars(app=None)
@pytest.fixture
def setup_app(scope="function"):
    if setup_app.app is None:
        setup_app.app = create_app("config/test_config.yml")
        setup_app.app.testing = True
    ctx = setup_app.app.app_context()
    ctx.push()
    dm.db.create_all()
    tmpfile = tempfile.mkstemp('test_log.log')[1]
    setup_app.app.config['log']['log_name'] = tmpfile
    logger(setup_app.app)
    yield setup_app.app
    dm.db.session.commit()
    dm.db.reflect()
    dm.db.drop_all()


@pytest.fixture
def fill_all_tables(setup_app, scope="function"):
    all_table_inputs = [
        dm.Store(store_name='Lifestyle'),
        dm.Store(store_name='Spar'),

        dm.Item(item_name='Apple'),
        dm.Item(item_name='Orange'),

    ]

    for table in all_table_inputs:
        dm.db.session.add(table)
    yield dm.db.session.commit()
