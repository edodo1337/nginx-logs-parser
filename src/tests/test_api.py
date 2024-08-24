import pytest
from django.test import Client
from django.urls import reverse_lazy
from tests.factories import NginxLogFactory


@pytest.fixture
def api_client():
    return Client()


@pytest.mark.django_db
def test_logs_list__ok(api_client):
    NginxLogFactory.create_batch(5)

    url = reverse_lazy("api-1.0.0:list_logs")
    response = api_client.get(url)
    response_data = response.json()

    assert response.status_code == 200
    assert "items" in response_data
    assert len(response_data["items"]) == 5

