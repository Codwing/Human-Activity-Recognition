# train_save_model.py
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import numpy as np
import pandas as pd

# Example training data (replace with your actual data)
X_train = np.random.rand(100, 10)  # Example feature data
y_train = np.random.choice(['class1', 'class2'], size=100)  # Example target data

# Create a pipeline with a scaler and classifier
model = make_pipeline(StandardScaler(), DecisionTreeClassifier())

# Train the model
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'model.pkl')
print("Model saved successfully.")
