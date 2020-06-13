import pytest
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.reverse import reverse

from test_app.factories import AFactory, BFactory


def test_get_a(client):
    a = AFactory()
    response = client.get(reverse('test_app_a-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1
    assert response.data['results'][0] == {
        "id": a.id,
        "name": a.name
    }


def test_create(client):
    request_data = {
        "name": "test_name"
    }
    response = client.post(reverse('test_app_a-list'), data=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == "test_name"


def test_update(client):
    a = AFactory()
    request_data = {
        "name": "test_name"
    }
    response = client.put(reverse('test_app_a-detail', kwargs={'pk': a.id}), data=request_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "test_name"


def test_delete(client):
    a = AFactory()
    response = client.delete(reverse('test_app_a-detail', kwargs={'pk': a.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(ObjectDoesNotExist):
        a.refresh_from_db()


def test_ordering(client):
    AFactory(name="ba")
    AFactory(name="ab")
    response = client.get(reverse('test_app_a-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'][0]['name'] == 'ba'
    assert response.data['results'][1]['name'] == 'ab'

    response = client.get(reverse('test_app_a-list'), data={'order_by': 'name'})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'][0]['name'] == 'ab'
    assert response.data['results'][1]['name'] == 'ba'


def test_filtering(client):
    AFactory(name="ba")
    AFactory(name="ab")
    AFactory(name="ab")

    response = client.get(reverse('test_app_a-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 3
    assert response.data['results'][0]['name'] == 'ba'
    assert response.data['results'][1]['name'] == 'ab'
    assert response.data['results'][1]['name'] == 'ab'

    response = client.get(reverse('test_app_a-list'), data={'name': 'ab'})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 2
    assert response.data['results'][0]['name'] == 'ab'
    assert response.data['results'][1]['name'] == 'ab'


def test_limit(client):
    [AFactory() for _ in range(3)]
    response = client.get(reverse('test_app_a-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 3
    assert len(response.data['results']) == 3

    response = client.get(reverse('test_app_a-list'), data={'limit': 1})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 3
    assert len(response.data['results']) == 1


def test_filtering_multiple_fields(client):
    a_first = AFactory()
    a_second = AFactory()
    b_first = BFactory(name='name', a=a_first)
    b_second = BFactory(name='name', a=a_second)
    b_third = BFactory(name='another_name', a=a_first)

    response = client.get(reverse('test_app_b-list'), data={'name': 'name'})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 2
    assert response.data['results'][0]['id'] == b_first.id
    assert response.data['results'][1]['id'] == b_second.id

    response = client.get(reverse('test_app_b-list'), data={'a': a_first.id})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 2
    assert response.data['results'][0]['id'] == b_first.id
    assert response.data['results'][1]['id'] == b_third.id

    response = client.get(reverse('test_app_b-list'), data={'name': 'name', 'a': a_first.id})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1
    assert response.data['results'][0]['id'] == b_first.id


def test_limit_filtering_is_not_working(client):
    b_first = BFactory(limit='value')
    b_second = BFactory(limit='another_value')

    response = client.get(reverse('test_app_b-list'), data={'limit': 1})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 2
    assert response.data['results'][0]['id'] == b_first.id
    assert len(response.data['results']) == 1

    response = client.get(reverse('test_app_b-list'), data={'limit': 'value'})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 2
    assert response.data['results'][0]['id'] == b_first.id
    assert response.data['results'][1]['id'] == b_second.id
