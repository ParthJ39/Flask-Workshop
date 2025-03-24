from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import re
from collections import Counter
import os
from werkzeug.utils import secure_filename
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoModelForSeq2SeqLM
import torch

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a proper secret key

# Initialize Hugging Face models
# Sentiment analysis model
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    return_all_scores=True
)

# Summarization model
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

# Text classification model (zero-shot classification)
text_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)


# Basic text processing functions
def count_words(text):
    """Count the number of words in a text."""
    words = re.findall(r'\b\w+\b', text.lower())
    return len(words)


def get_word_frequency(text, top_n=10):
    """Get the frequency of words in a text."""
    words = re.findall(r'\b\w+\b', text.lower())
    # Remove common stop words
    stop_words = {'the', 'and', 'a', 'to', 'in', 'of', 'is', 'that', 'it', 'for', 'with', 'as', 'on', 'was', 'be',
                  'this', 'are'}
    filtered_words = [word for word in words if word not in stop_words]
    word_freq = Counter(filtered_words)
    return word_freq.most_common(top_n)


# Advanced analysis functions using Hugging Face models
def huggingface_sentiment_analysis(text):
    """Use Hugging Face model for sentiment analysis."""
    # Limit text length to avoid model issues with very long texts
    max_length = 512
    if len(text) > max_length:
        text = text[:max_length]

    # Get sentiment prediction
    results = sentiment_analyzer(text)

    # Extract scores from results
    # Format is typically [{'label': 'POSITIVE', 'score': 0.999}, {'label': 'NEGATIVE', 'score': 0.001}]
    scores = {result['label'].lower(): result['score'] for result in results[0]}

    # Determine overall sentiment
    if scores.get('positive', 0) > scores.get('negative', 0):
        return "Positive", scores.get('positive', 0), scores.get('negative', 0)
    else:
        return "Negative", scores.get('positive', 0), scores.get('negative', 0)


def generate_summary(text, max_length=150):
    """Generate a summary of the text using Hugging Face model."""
    # Check text length
    if len(text) < 50:
        return ["Text too short for summarization."]

    # Generate summary
    summary = summarizer(
        text,
        max_length=max_length,
        min_length=30,
        do_sample=False
    )

    # Extract summary text
    summary_text = summary[0]['summary_text']

    # Split into sentences (simple approach)
    sentences = summary_text.split('. ')
    return [s + '.' for s in sentences if s]


def classify_text(text, labels=["business", "science", "politics", "entertainment", "technology"]):
    """Classify text into predefined categories."""
    # For longer texts, truncate to avoid model issues
    max_length = 1024
    if len(text) > max_length:
        text = text[:max_length]

    # Perform zero-shot classification with all labels at once
    try:
        prediction = text_classifier(
            sequences=text,
            candidate_labels=labels,
            multi_class=True
        )

        # The response format is different than expected - it returns a single dict
        # with 'labels' and 'scores' keys rather than a list of dicts
        results = []
        for i, label in enumerate(prediction['labels']):
            results.append({
                "topic": label,
                "score": prediction['scores'][i]
            })

        # Sort by score (highest first)
        results = sorted(results, key=lambda x: x['score'], reverse=True)
        return results
    except Exception as e:
        # Fallback in case of errors
        print(f"Classification error: {e}")
        return [{"topic": label, "score": 0.2} for label in labels]


# Routes
@app.route('/')
def index():
    """Render the home page."""
    # Get analysis history from session
    history = session.get('history', [])
    return render_template('index.html', history=history)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis."""
    # Check if a file was uploaded
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    # If no file selected
    if file.filename == '':
        return redirect(request.url)

    if file:
        # Read the file content
        content = file.read().decode('utf-8')

        # Process the text
        word_count = count_words(content)
        word_freq = get_word_frequency(content)

        # Use Hugging Face models for analysis
        sentiment, pos_score, neg_score = huggingface_sentiment_analysis(content)
        summary = generate_summary(content)
        topics = classify_text(content)

        # Store analysis in session
        session['analysis'] = {
            'filename': file.filename,
            'word_count': word_count,
            'word_freq': word_freq,
            'sentiment': sentiment,
            'pos_score': round(pos_score * 100, 2),
            'neg_score': round(neg_score * 100, 2),
            'summary': summary,
            'topics': topics[:3],  # Top 3 topics
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Add to history
        if 'history' not in session:
            session['history'] = []

        # Add simplified version to history
        history_item = {
            'filename': file.filename,
            'word_count': word_count,
            'sentiment': sentiment,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        session['history'] = [history_item] + session['history']
        # Limit history size
        if len(session['history']) > 5:
            session['history'] = session['history'][:5]

        return redirect(url_for('results'))


@app.route('/results')
def results():
    """Display analysis results."""
    # Get analysis from session
    analysis = session.get('analysis')
    if not analysis:
        return redirect(url_for('index'))

    return render_template('results.html', analysis=analysis)


@app.route('/clear-history')
def clear_history():
    """Clear analysis history."""
    session.pop('history', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)