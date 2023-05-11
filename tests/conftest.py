import pytest

from src.api import create_app


@pytest.fixture()
def app():
    """Create instance of Flask App for tests."""
    app = create_app()
    app.config.update({
        'TESTING': True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    """Returns the test-client."""
    return app.test_client()


@pytest.fixture()
def runner(app):
    """Returns the test-client runner."""
    return app.test_cli_runner()
