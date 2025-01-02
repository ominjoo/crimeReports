import pandas as pd
from cleaning import clean_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

df = pd.read_csv("ucsd_crime_data_encoded.csv")

# prepare features/training variables, split data into training/testing
X = df[['time', 'location_frequency']]
y = df['crime_category']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("Evaluating the model...")
y_pred = model.predict(X_test)

# Output the classification report and accuracy
print(f'Accuracy: {accuracy_score(y_test, y_pred):.2f}')
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the trained model to a file for later use
joblib.dump(model, 'crime_predictor_rf_model.pkl')
print("Model saved as 'crime_predictor_rf_model.pkl'")