from flask import Flask, request, jsonify, render_template
from tweet_fetcher import fetch_tweets_async  # Import fetch_tweets_async function
import asyncio

# Initialize Flask app
app = Flask(__name__)

# Route for the root URL ("/")
@app.route('/')
def index():
    # Render the HTML file for the frontend
    return render_template('tweets.html')

# Route to handle tweet fetching based on query
@app.route('/fetch_tweets', methods=['POST'])
def fetch_tweets():
    query = request.json.get('query', '')  # Get the query from the request
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Run the asynchronous tweet fetching function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tweets = loop.run_until_complete(fetch_tweets_async(query))

    return jsonify(tweets)

if __name__ == '__main__':
    app.run(debug=True)
