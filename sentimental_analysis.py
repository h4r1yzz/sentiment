# sentimental_analysis.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from transformers import logging
logging.set_verbosity_error()

# Sentiment analysis function (based on tweet.text)
def get_sentiment(tweet):
    # No need for preprocessing, use the tweet text as-is
    tweet_proc = tweet

    # Load the sentiment analysis model
    roberta = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    # Define sentiment labels
    labels = ['Negative', 'Neutral', 'Positive']

    # Tokenize the processed tweet
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')

    # Run the model on the tweet
    output = model(**encoded_tweet)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    # Output the sentiment probabilities and convert to native Python float for serialization
    sentiment = {}
    for i in range(len(scores)):
        sentiment[labels[i]] = round(float(scores[i]), 4)  # Convert to Python float

    return sentiment
