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

X-API-Key: <your-api-key>

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
API_KEY=<your-api-key>
```

## Run the API

### Local Development

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1

## API Endpoints

### Health Check

GET /api/v1/health

API and ML model available-aa irukka check pannum.

Requires:
X-API-Key


### Prediction

POST /api/v1/predict

Given iris measurements based on iris class predict pannum.

Requires:
X-API-Key


### Batch Prediction

POST /api/v1/predict-batch

Multiple iris samples-a ore request-la predict pannum.

Requires:
X-API-Key


### Model Information

GET /api/v1/model-info

Loaded ML model-oda information return pannum.

Requires:
X-API-Key


### Metrics

GET /metrics

Prometheus monitoring metrics-a return pannum.
