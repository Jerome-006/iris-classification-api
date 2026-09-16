# Testing

## Test Environment

- Python: 3.11.9
- Framework: FastAPI
- Test Framework: pytest
- HTTP Client: httpx
- Test Client: FastAPI TestClient

## Automated Tests

The project uses pytest and FastAPI TestClient for automated API testing.

Run all tests with:

```bash
python -m pytest -v

## Load Test Result

A basic load test was performed by sending 20 consecutive prediction requests to the `/api/v1/predict` endpoint.

- Total requests: 20
- Successful requests: 20
- Failed requests: 0
- Total execution time: 0.177 seconds

Result: All 20 requests were successful.