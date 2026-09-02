def test_predict_batch_oversized(client):
    payload = {
        "inputs": [
            {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        ] * 11
    }

    response = client.post("/api/v1/predict-batch", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Maximum batch size is 10"