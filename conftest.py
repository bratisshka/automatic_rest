import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope='session')
def client(django_db_setup, django_db_blocker):
    client = APIClient()
    return client


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker('django_db')
