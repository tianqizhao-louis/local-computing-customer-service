import pytest


@pytest.mark.asyncio
async def test_database_connection(test_database):
    """Test that we're using SQLite in memory database"""
    # Check if the connection is SQLite
    assert str(test_database.url).startswith("sqlite:")
    assert "memory" in str(test_database.url)

    # Verify we can execute a simple query
    query = (
        "SELECT 1;"  # Changed to a simpler query that works in both SQLite and Postgres
    )
    result = await test_database.fetch_one(query)
    assert result is not None


@pytest.fixture
def sample_customer():
    return {"name": "Test Customer", "email": "test@gmail.com"}


@pytest.fixture
def updated_customer():
    return {"name": "Updated Customer", "email": "update@gmail.com"}


@pytest.mark.asyncio
async def test_get_customers(test_client):
    response = test_client.get("/api/v1/customers/")
    assert response.status_code == 200
    assert response.json()["links"] is not None


@pytest.mark.asyncio
async def test_create_and_get_customer(test_client, sample_customer):
    # Create a breeder
    response = test_client.post("/api/v1/customers/", json=sample_customer)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == sample_customer["name"]
    assert data["email"] == sample_customer["email"]
    assert "id" in data

    # Verify it was created
    get_response = test_client.get("/api/v1/customers/")
    assert get_response.status_code == 200
    assert len(get_response.json()["data"]) == 1

    # Get specific breeder
    get_one_response = test_client.get(f"/api/v1/customers/{data['id']}")
    assert get_one_response.status_code == 200
    assert get_one_response.json() == data


@pytest.mark.asyncio
async def test_update_customer(test_client, sample_customer, updated_customer):
    create_response = test_client.post("/api/v1/customers/", json=sample_customer)
    assert create_response.status_code == 201
    customer_id = create_response.json()["id"]

    # Update the breeder
    update_response = test_client.put(
        f"/api/v1/customers/{customer_id}", json=updated_customer
    )
    assert update_response.status_code == 200

    updated_data = update_response.json()
    assert updated_data["name"] == updated_customer["name"]
    assert updated_data["email"] == updated_customer["email"]

    # Verify the update
    get_response = test_client.get(f"/api/v1/customers/{customer_id}")
    assert get_response.status_code == 200
    assert get_response.json() == updated_data


@pytest.mark.asyncio
async def test_update_customer_invalid_id(test_client, updated_customer):
    response = test_client.put("/api/v1/customers/invalid-id", json=updated_customer)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_customer(test_client, sample_customer):
    create_response = test_client.post("/api/v1/customers/", json=sample_customer)
    assert create_response.status_code == 201
    customer_id = create_response.json()["id"]

    # Delete the breeder
    delete_response = test_client.delete(f"/api/v1/customers/{customer_id}")
    assert delete_response.status_code == 200

    # Verify the breeder was deleted
    get_response = test_client.get(f"/api/v1/customers/{customer_id}")
    assert get_response.status_code == 404

    # Verify the breeder is not in the list
    list_response = test_client.get("/api/v1/customers/")
    assert list_response.status_code == 200
    assert len(list_response.json()["data"]) == 0


@pytest.mark.asyncio
async def test_delete_customer_invalid_id(test_client):
    response = test_client.delete("/api/v1/customers/invalid-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_customer_invalid_data(test_client):
    response = test_client.get("/api/v1/customers/123")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_cleanup_between_tests(test_client, test_database):
    """Verify that the database is clean between tests"""
    # This should be empty as it's a fresh database
    response = test_client.get("/api/v1/customers/")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 0
