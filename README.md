# Iris Classification API

## Project Plan

This project builds a simple Machine Learning API using the Iris dataset from scikit-learn.

### Goal

Predict the species of an iris flower using four measurements:

- Sepal Length
- Sepal Width
- Petal Length
- Petal Width

### Model

Scikit-learn Iris Classifier

### API Output

- Predicted flower species
- Confidence score

## How to Run This Project

### Prerequisites

Make sure Docker Desktop is installed and running.

## Security

### API Key Authentication

All prediction API endpoints require a valid `X-API-Key` header.

The API key is stored in the environment configuration and is never hardcoded in the application code.

Example:

X-API-Key: my-dev-api-key-2026

Requests without a valid API key are rejected with HTTP status code 401 Unauthorized.

### Input Validation

The API validates prediction inputs before processing:

- All measurement values must be greater than 0.
- Measurement values must be less than 100.
- Empty or non-numeric values are rejected.
- Unexpected fields are rejected using Pydantic extra="forbid".

Invalid input requests return HTTP status code 422 Unprocessable Entity.

### CORS

CORS is explicitly configured.

Allowed browser origin:

http://localhost:3000

Only the required HTTP methods and headers are allowed.

### Rate Limiting

Rate limiting is not currently implemented inside the application.

For production deployment, rate limiting should be configured using an API gateway, reverse proxy, or dedicated rate-limiting middleware to prevent excessive requests and API abuse.

### Environment Configuration

Create a `.env` file in the project root with:

```env
MODEL_PATH=ml/saved_model/model.joblib
MODEL_METADATA_PATH=ml/saved_model/metadata.json
LOG_LEVEL=INFO
MAX_BATCH_SIZE=10
API_TITLE=Iris Classification API
