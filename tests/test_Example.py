import pytest

from src.api import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_json_data(client):
    response = client.get('/api/hello')
    assert (
        response.json['content'] ==
        'hello, i am running the hello function of exchange.py'
    )
