import pytest

from ...app import app, businesses, users, service

@pytest.fixture(autouse=True)
def reset_data():
    businesses.clear()
    users.clear()
    service.bookings.clear()
    yield
    businesses.clear()
    users.clear()
    service.bookings.clear()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client