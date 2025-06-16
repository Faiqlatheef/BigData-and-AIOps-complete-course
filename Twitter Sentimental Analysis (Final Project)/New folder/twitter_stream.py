import tweepy
from kafka import KafkaProducer
import json
import time

# Twitter API credentials
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHy%2FugEAAAAASuKZiULDBj65SEbXkqav6a8Fa7A%3DHjCzCYt5MoMdpUqgwG8cEqwtIqAskGFnWeOY56bUYFQXkiGnyo'

# Kafka configuration
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
topic_name = 'twitter_stream'

# Set up Twitter API client
client = tweepy.Client(bearer_token=bearer_token)

def fetch_and_send_tweets():
    query = "keyword"  # Replace with your desired keyword or query
    while True:
        response = client.search_recent_tweets(query=query, tweet_fields=['text'], max_results=10)
        if response.data:
            for tweet in response.data:
                producer.send(topic_name, tweet.text)
                print(f"Tweet sent to Kafka: {tweet.text}")
        time.sleep(60)  # Fetch tweets every 60 seconds

if __name__ == "__main__":
    fetch_and_send_tweets()
