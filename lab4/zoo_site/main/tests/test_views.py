import pytest
from django.urls import reverse
from constants import BASE_VIEWS, SPECIFIC_VIEWS


@pytest.mark.parametrize('view', BASE_VIEWS)
@pytest.mark.django_db
def test_general_access(user, client, view):
    if isinstance(view, tuple):
        response = client.get(reverse(view[0], kwargs={'id': 1}))
    else:
        response = client.get(reverse(view))
    assert response.status_code == 200

    client.force_login(user)
    if isinstance(view, tuple):
        response = client.get(reverse(view[0], kwargs={'id': 1}))
    else:
        response = client.get(reverse(view))
    assert response.status_code == 200


@pytest.mark.parametrize('view', SPECIFIC_VIEWS)
@pytest.mark.django_db
def test_user_access(user, client, view):
    client.force_login(user)
    if isinstance(view, tuple):
        response = client.get(reverse(view[0], kwargs={'pk': 1}))
    else:
        response = client.get(reverse(view))
    assert response.status_code == 200


@pytest.mark.parametrize('view', SPECIFIC_VIEWS)
@pytest.mark.django_db
def test_nonuser_access(client, view):
    if isinstance(view, tuple):
        response = client.get(reverse(view[0], kwargs={'pk': 1}))
    else:
        response = client.get(reverse(view))
    assert response.status_code == 302
