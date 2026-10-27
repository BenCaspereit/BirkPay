def test_admin_can_create_and_list_products(
    client,
    role_headers,
    product_factory,
):
    create_response = client.post(
        "/api/v1/products/",
        headers=role_headers("admin"),
        json={"name": "Water", "price_cents": 125},
    )

    assert create_response.status_code == 201
    created_product = create_response.json()
    assert created_product["name"] == "Water"
    assert created_product["price_cents"] == 125

    product_factory(name="Inactive", is_active=False)
    list_response = client.get("/api/v1/products/")

    assert list_response.status_code == 200
    assert [product["name"] for product in list_response.json()] == ["Water"]

    all_response = client.get("/api/v1/products/", params={"only_active": False})
    assert all_response.status_code == 200
    assert {product["name"] for product in all_response.json()} == {"Water", "Inactive"}


def test_non_admin_cannot_create_product(client, role_headers):
    response = client.post(
        "/api/v1/products/",
        headers=role_headers("cashier"),
        json={"name": "Forbidden", "price_cents": 100},
    )

    assert response.status_code == 403


def test_create_product_rejects_invalid_payload(client, role_headers):
    response = client.post(
        "/api/v1/products/",
        headers=role_headers("admin"),
        json={"name": "Missing price"},
    )

    assert response.status_code == 422


def test_get_product_returns_404_for_unknown_product(client):
    response = client.get("/api/v1/products/9999")

    assert response.status_code == 404


def test_deactivate_product_hides_it_from_active_list(
    client,
    role_headers,
    product_factory,
):
    product = product_factory(name="To deactivate")

    response = client.delete(
        f"/api/v1/products/{product.id}",
        headers=role_headers("admin"),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False
    assert client.get("/api/v1/products/").json() == []
