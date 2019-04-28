import pytest
from mongoengine import connect


@pytest.fixture
def setup_mongo():
    connect(host='mongomock://localhost', db='graphene-mongo-extras')
