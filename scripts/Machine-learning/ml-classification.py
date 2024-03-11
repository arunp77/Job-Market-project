import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# File path of adzuna_scrapped_data.csv
file_path = '../../data/scraped_data/adjurna/csv/adzuna_scrapped_data.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)


# Select features and target
X = df['description']  # 'Description' column contains the lengthy text
y = df['category']  # Assuming 'Categories' column contains the predefined categories


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize the text data
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train the classifiers
classifiers = {
    'Naive Bayes': MultinomialNB(),
    'Support Vector Machine (SVM)': SVC(),
    'Random Forest': RandomForestClassifier()
}


# Initialize lists to store classifier names and accuracies
classifier_names = []
accuracies = []

for clf_name, clf in classifiers.items():
    clf.fit(X_train_vectorized, y_train)
    y_pred = clf.predict(X_test_vectorized)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    classifier_names.append(clf_name)
    accuracies.append(accuracy)

    # Print classification report
    print(f'{clf_name} Classification Report:')
    print(classification_report(y_test, y_pred))
    
    
# Plotting
plt.figure(figsize=(10, 6))
plt.bar(classifier_names, accuracies, color=['blue', 'green', 'orange'])
plt.xlabel('Classifier')
plt.ylabel('Accuracy')
plt.title('Classifier Performance Comparison')
plt.ylim(0, 1)  # Set y-axis limits

# Save the plot as an image file
plot_file_path = 'classifier_performance_comparison.png'  # Set the directory where you want to save the plot
plt.savefig(plot_file_path)

# Display the plot as a pop-up window
plt.show()