from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import json
from datetime import date

# Load Database
iris = load_iris()
x = iris.data
y = iris.target

# Split Dataset
X_train, X_tests, y_train, y_tests = train_test_split(
    x, y, test_size=0.2, random_state=42
)

# Train Model 
model = RandomForestClassifier(random_state=42)
model.fit(X_train,y_train)

# Test Accuracy
predictions = model.predict(X_tests)
accuracy = accuracy_score(y_tests,predictions)
print("Accuracy:", accuracy)

# Model Metadata
metadata = {
    "model_type": type(model).__name__,
    "version": "1.0.0",
    "training_date": str(date.today()),
    "expected_features": [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width"
    ],
    "accuracy": accuracy
}

# Save Model
joblib.dump(model, "ml/saved_model/model.joblib")
print("Model saved")

with open("ml/saved_model/metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

print("Metadata saved")