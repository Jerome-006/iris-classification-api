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

### Environment Configuration

Create a `.env` file in the project root with:

```env
MODEL_PATH=ml/saved_model/model.joblib
MODEL_METADATA_PATH=ml/saved_model/metadata.json
LOG_LEVEL=INFO
MAX_BATCH_SIZE=10
API_TITLE=Iris Classification API
