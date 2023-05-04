import pytest

from src.api import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_bus_data(client):
    response = client.get('/api/bus')
    assert (
        response.json['bus_data'] is not None
    )


def test_stop_data(client):
    response = client.get('/api/bus')
    assert (
        response.json['stop_data'] is not None
    )
