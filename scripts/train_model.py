from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load preprocessed data
X_train, X_test, y_train, y_test = joblib.load('../data/processed_data.pkl')

# Initialize and train the Random Forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict clearly on test data
predictions = model.predict(X_test)

# Display model performance clearly
print("Classification Report:\n", classification_report(y_test, predictions))

# Save your trained model clearly
joblib.dump(model, '../models/sql_injection_rf_model.pkl')

print("Model training completed and saved successfully.")
