# Iris Classification API

A production-style Machine Learning REST API built with FastAPI for classifying Iris flowers using a Scikit-learn Random Forest model.

The API accepts four Iris flower measurements and returns the predicted class, confidence score, and request ID.

---

## Project Overview

### Goal

The goal of this project is to build and deploy a reliable Machine Learning API that can:

- Accept Iris flower measurements through REST API endpoints
- Predict the Iris class using a trained Scikit-learn model
- Provide prediction confidence
- Support single and batch predictions
- Provide API versioning
- Protect prediction endpoints using API key authentication
- Validate incoming request data
- Expose Prometheus-compatible monitoring metrics
- Run reproducibly using Docker Compose
- Support automated testing and CI

### Input Features

The model uses four measurements:

- Sepal Length
- Sepal Width
- Petal Length
- Petal Width

### Machine Learning Model

The project uses a Scikit-learn `RandomForestClassifier`.

Model metadata is stored in:

```text
ml/saved_model/metadata.json