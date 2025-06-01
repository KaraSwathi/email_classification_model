import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from joblib import dump

# Load dataset
df = pd.read_csv("combined_emails_with_natural_pii.csv")  # Ensure dataset contains 'text' and 'category'

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(df["email"], df["type"], test_size=0.2, random_state=42)

# Convert text into numerical features using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train Naïve Bayes Model
nb_model = MultinomialNB()
nb_model.fit(X_train_tfidf, y_train)

# Evaluate Model
y_pred_nb = nb_model.predict(X_test_tfidf)
nb_accuracy = accuracy_score(y_test, y_pred_nb)
print(f"Naïve Bayes Accuracy: {nb_accuracy:.2f}")

# Save trained models
dump(vectorizer, "vectorizer.joblib")
dump(nb_model, "nb_email_classifier.joblib")