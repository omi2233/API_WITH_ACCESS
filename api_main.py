from flask import Flask, request, jsonify
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import nltk
import json
from functools import wraps

app = Flask(__name__)

# Load cache from file
cache_file = "cache.json"
try:
    with open(cache_file, "r") as f:
        cache = json.load(f)
except FileNotFoundError:
    cache = {}


def perform_search(query):
    try:
        print('\nSearching web .........\n\n')
        results = list(search(query, num_results=6))
        return results
    except Exception as e:
        print("An error occurred during the search:", e)
        return []


def summarize_text(text):
    try:
        print("Summarizing and preparing the content to display ...........\n\n")
        sentences = sent_tokenize(text)
        word_frequencies = FreqDist([word for word in text.lower().split() if word not in stopwords.words('english')])
        ranking = {}
        for i, sentence in enumerate(sentences):
            for word in sentence.lower().split():
                if word in word_frequencies:
                    if i in ranking:
                        ranking[i] += word_frequencies[word]
                    else:
                        ranking[i] = word_frequencies[word]

        sorted_sentences = sorted(ranking, key=ranking.get, reverse=True)
        top_sentences = sorted_sentences[:3]
        summary = ' '.join([sentences[i] for i in top_sentences])
        return summary
    except Exception as e:
        print("An error occurred during text summarization:", e)
        return ""


def verify_api_key(api_key):
    # Implement your API key verification logic here
    # For example, you can check if the provided API key is valid in your system/database
    valid_keys = ["your_api_key_1", "your_api_key_2", "your_api_key_3"]  # Replace with your valid API keys
    return api_key in valid_keys


def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.args.get('api_key')
        if not api_key:
            return jsonify({'error': 'API key is missing.'}), 400
        if not verify_api_key(api_key):
            return jsonify({'error': 'Invalid API key.'}), 401
        return f(*args, **kwargs)

    return decorated_function


@app.route('/search', methods=['GET'])
@api_key_required
def search_api():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is missing.'}), 400

    if query in cache:
        return jsonify({'summary': cache[query]})

    results = perform_search(query)
    text = ""
    if results:
        print('Getting content...........\n\n')
        for url in results[:3]:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                paragraphs = soup.find_all('p')
                for paragraph in paragraphs:
                    text += paragraph.text
            except Exception as e:
                print("An error occurred while scraping the web page:", e)
    if text:
        summary = summarize_text(text)
        cache[query] = summary
        with open(cache_file, "w") as f:
            json.dump(cache, f)
        return jsonify({'summary': summary})
    else:
        return jsonify({'error': 'No content found for the search query.'}), 404


if __name__ == '__main__':

    app.run()
