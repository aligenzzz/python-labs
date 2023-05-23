import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_animal_crud_view(user, client):
    client.force_login(user)

    form_data = {'name': 'Lina'}
    response = client.post(reverse('add_animal'), data=form_data)
    assert response.status_code == 200

    form_data = {'name': 'Ilina'}
    response = client.post(reverse('edit_animal', kwargs={'pk': 2}), data=form_data)
    assert response.status_code == 200

    response = client.post(reverse('delete_animal', kwargs={'pk': 2}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_placement_crud_view(user, client):
    client.force_login(user)

    form_data = {
        'number': 1,
        'name': 'Test',
        'basin': True,
        'area': 222
    }
    response = client.post(reverse('add_placement'), data=form_data)
    assert response.status_code == 302

    form_data = {'name': 'TEST'}
    response = client.post(reverse('edit_placement', kwargs={'pk': 2}), data=form_data)
    assert response.status_code == 200

    response = client.post(reverse('delete_animal', kwargs={'pk': 2}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_edit_view(user, client):
    client.force_login(user)

    form_data = {'firstname': 'Kolya'}
    response = client.post(reverse('user_settings'), data=form_data)
    assert response.status_code == 302



