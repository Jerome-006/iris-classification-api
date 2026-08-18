from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

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

# Save Model
joblib.dump(model, "ml/saved_model/model.joblib")
print("Model saved")