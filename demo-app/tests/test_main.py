def test_root_endpoint(client):
    """Test the root endpoint for correct metadata and status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert "Bhupender Gaur" in data["message"]
    assert data["version"] == "0.1.0"


def test_health_check(client):
    """Test the liveness/health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_read_item(client):
    """Test the /items/{item_id} endpoint without query params."""
    response = client.get("/items/42")
    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == 42
    assert data["q"] is None
    assert data["p"] is None


def test_read_item_with_query_params(client):
    """Test the /items/{item_id} endpoint with query params."""
    response = client.get("/items/101?q=searchterm&p=filterparam")
    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == 101
    assert data["q"] == "searchterm"
    assert data["p"] == "filterparam"
