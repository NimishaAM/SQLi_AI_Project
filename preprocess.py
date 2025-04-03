import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import joblib

# Load your dataset
df = pd.read_csv('../data/sql_injection_data.csv')

# Extract features and labels
X_text = df['Query']
y = df['Label']

# Convert text into numerical features using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(X_text).toarray()

# Split data into training and testing sets (80:20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Save the processed data & vectorizer clearly for later use
joblib.dump((X_train, X_test, y_train, y_test), '../data/processed_data.pkl')
joblib.dump(vectorizer, '../models/vectorizer.pkl')

print("Data preprocessing complete. Files saved successfully.")
