from flask import Flask, request, render_template, redirect, url_for, session
import pickle
import threading
import webbrowser
import phishing_keywords as pk_data
import pandas as pd
import re
from nltk import ngrams

# Load the phishing detection model from the .pkl file
model_path = r'svc_model_latest.pkl'
with open(model_path, 'rb') as file:
    phishing_model = pickle.load(file)  # Load the model

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Dictionary of valid usernames and passwords for the login system
VALID_USERS = {
    'admin': 'password',
    'luke': '123456',
    'wayne': 'iamgay'
    # Add more users and passwords here
}

def text_preprocessing(text):
    # Regex pattern to remove URLs and emails for better normalization
    url_email_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|'
        r'www\.[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}|'
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', re.IGNORECASE
    )
    # Remove any URLs or emails for more normalization
    text = re.sub(url_email_pattern, '', text)
    # Replace apostrophes with an empty string
    text = text.replace("'", '')
    # Remove email prefixes (Fw/Re)
    text = re.sub(r'(?<!\w)(fw|re)(?=\s*:?)\s*:?\s+', '', text, flags=re.IGNORECASE)
    # Remove punctuations - replace with space instead of empty string to account for stemming
    text = re.sub(r'[^\w\s]|[_-]', ' ', text)
    # Replace multiple spaces, tabs(\t), newlines(\n) with a single space for uniformity and strip surrounding whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Return the processed text
    return text


def calc_caps_percent(text):
    # Count total alphabetical letters
    total_chars = sum(c.isalpha() for c in text)  # Count total alphabetical letters
    # Count uppercase letters
    capital_chars = sum(c.isupper() for c in text)  # Count uppercase letters
    # Calculate the percentage
    return round((capital_chars / total_chars * 100), 2) if total_chars > 0 else 0


def calc_word_count(text):
    # Split the text into words and filter out numbers
    words = [word for word in text.split() if not word.isdigit()]

    # Return the count of words
    return len(words)


def count_matching_ngrams(text, n):
    if n == 1:
        ngram_dict_data = pk_data.unigrams.values()
    elif n == 2:
        ngram_dict_data = pk_data.bigrams.values()
    else:
        ngram_dict_data = pk_data.trigrams.values()
    # Convert the text to lowercase and split into words
    words = text.lower().split()

    # Generate n-grams from the words
    generated_ngram = ngrams(words, n)

    # Count the number of matching n-grams
    count = 0
    for ngram in generated_ngram:
        ngram_string = ' '.join(ngram)
        # Check if the n-gram is in the provided ngram dictionary
        if any(ngram_string in sus_ngram for sus_ngram in ngram_dict_data):
            count += 1
    return count


def calc_composite_score(unigram_count, bigram_count, trigram_count):
    unigram_weight = 0.1667
    bigram_weight = 0.3333
    trigram_weight = 0.5
    return (unigram_weight * unigram_count) + (bigram_weight * bigram_count) + (trigram_weight * trigram_count)


def extract_features(subject, body):
    # Regex pattern to check for urls in email body and save as url_label
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|www\.[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}'
    url_label = 1 if re.search(url_pattern, body) else 0

    # Apply Text Preprocessing on Subject/Body after checking if url exists
    subject = text_preprocessing(subject)
    body = text_preprocessing(body)

    # Calculate Caps Percentage for Subject/Body
    subject_caps_percent = calc_caps_percent(subject)
    body_caps_percent = calc_caps_percent(body)

    # Calculate Word Count for Subject/Body
    subject_word_count = calc_word_count(subject)
    body_word_count = calc_word_count(body)

    # Count Matching Ngrams
    unigram_count = count_matching_ngrams(subject + ' ' + body, 1)
    bigram_count = count_matching_ngrams(subject + ' ' + body, 2)
    trigram_count = count_matching_ngrams(subject + ' ' + body, 3)

    unigram_percent = unigram_count / (subject_word_count + body_word_count) * 100 if (
                                                                                                  subject_word_count + body_word_count) > 0 else 0

    composite_score = calc_composite_score(unigram_count, bigram_count, trigram_count)

    return [subject_caps_percent, body_caps_percent, subject_word_count, body_word_count,
            unigram_count, bigram_count, trigram_count, unigram_percent, composite_score, url_label]


# Function to predict phishing based on the extracted features
def predict_phishing(subject, body):
    try:
        # Extract features from the subject and body
        features = extract_features(subject, body)

        features_df = pd.DataFrame([features],
                                   columns=['subject_caps_percent', 'body_caps_percent', 'subject_word_count',
                                            'body_word_count', 'unigram_count', 'bigram_count', 'trigram_count',
                                            'unigram_percent', 'composite_score', 'url_label'])

        # Make the prediction using the model
        prediction = phishing_model.predict(features_df)

        return f"PHISHING" if prediction[0] == 1 else f"NOT PHISHING"
    except Exception as e:
        print(f"Error during prediction: {e}")
        return f"An error occurred during prediction: {e}"


# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists and the password matches
        if username in VALID_USERS and VALID_USERS[username] == password:
            session['logged_in'] = True
            session['username'] = username  # Store the username in the session
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password, please try again."

    return render_template('login.html', error=error)

# Define the main page route
@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    subject = ""
    body = ""
    result = ""
    if request.method == 'POST':
        # Pass Subject & Body to Predict Phishing Function
        subject = request.form['subject']
        body = request.form['body']
        result = predict_phishing(subject, body)

        # Give final display msg
        subject = 'Subject: ' + subject
        body = 'Body: ' + body
        result = 'Result: ' + result
    return render_template('index.html', result=result, subject=subject, body=body)


# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)  # Clear the username from the session
    return redirect(url_for('login'))


# Class to run the Flask app in a separate thread
class FlaskThread(threading.Thread):
    def run(self):
        app.run(host='localhost', port=5001)


# Run the Flask app in a new thread
flask_thread = FlaskThread()
flask_thread.start()

# Open the web app in the default browser
webbrowser.open('http://localhost:5001/')
