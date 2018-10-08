def test_logging_requests(setup_app):
    client = setup_app.test_client()
    client.post("/")
    test_file = open(setup_app.config['log']['log_name'])
    last_line = test_file.readlines()[-1]
    assert "REQUEST: " in last_line
