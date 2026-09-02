import pytest

def test_v1_and_v2_response_shapes(client):

    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    v1_response = client.post(
        "/api/v1/predict",
        json=payload
    )

    v2_response = client.post(
        "/api/v2/predict",
        json=payload
    )

    assert v1_response.status_code == 200
    assert v2_response.status_code == 200

    v1_data = v1_response.json()
    v2_data = v2_response.json()

    # V1 must keep its original response shape
    assert set(v1_data.keys()) == {
        "prediction",
        "confidence",
        "request_id"
    }

    # V2 intentionally has a different response shape
    assert set(v2_data.keys()) == {
        "prediction",
        "probabilities",
        "request_id"
    }

    # Both versions should make the same prediction
    assert v1_data["prediction"] == v2_data["prediction"]

    # V2 must return a probability distribution
    assert isinstance(v2_data["probabilities"], list)
    assert len(v2_data["probabilities"]) == 3

    assert all(
        0.0 <= probability <= 1.0
        for probability in v2_data["probabilities"]
    )

    assert sum(v2_data["probabilities"]) == pytest.approx(1.0)

    # Prove the breaking field change
    assert "confidence" not in v2_data
    assert "probabilities" not in v1_data