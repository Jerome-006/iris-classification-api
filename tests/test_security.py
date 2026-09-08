from app.config import settings


def test_predict_missing_api_key(client):
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    response = client.post(
        "/api/v1/predict",
        json=payload
    )

    assert response.status_code == 401


def test_predict_invalid_api_key(client):
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    response = client.post(
        "/api/v1/predict",
        json=payload,
        headers={"X-API-Key": "wrong-api-key"}
    )

    assert response.status_code == 401


def test_predict_rejects_extra_field(client):
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
        "extra_field": "not allowed"
    }

    response = client.post(
        "/api/v1/predict",
        json=payload,
        headers={"X-API-Key": settings.API_KEY}
    )

    assert response.status_code == 422


def test_predict_rejects_negative_value(client):
    payload = {
        "sepal_length": -5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    response = client.post(
        "/api/v1/predict",
        json=payload,
        headers={"X-API-Key": settings.API_KEY}
    )

    assert response.status_code == 422


def test_predict_rejects_extreme_value(client):
    payload = {
        "sepal_length": 999999,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    response = client.post(
        "/api/v1/predict",
        json=payload,
        headers={"X-API-Key": settings.API_KEY}
    )

    assert response.status_code == 422


def test_predict_rejects_empty_string(client):
    payload = {
        "sepal_length": "",
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    response = client.post(
        "/api/v1/predict",
        json=payload,
        headers={"X-API-Key": settings.API_KEY}
    )

    assert response.status_code == 422
