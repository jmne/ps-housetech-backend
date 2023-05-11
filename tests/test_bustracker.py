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


def test_bustracker_data(client):
    response = client.get('/api/bus')
    assert len(response) <= 6
    assert response[0].json['station'] == 'Leonardo-Campus'
