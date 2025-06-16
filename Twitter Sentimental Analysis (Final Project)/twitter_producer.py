# twitter_producer.py

import tweepy
from kafka import KafkaProducer
import json

# Twitter API credentials
API_KEY = 'kNvL7zeB0xgLtj197raF86h77'
API_SECRET_KEY = 'vgmkp0V48jE3BjktvEcetIGUHhbS1aCKtVTzw9LekzhCitPsiL'
ACCESS_TOKEN = '718316988-d3JVokui0Z38pF7ga1QbnqtCiWiSnbSqvzjnGb9b'
ACCESS_TOKEN_SECRET = 'HnDoS2IOH6tugekaottWdJ8xDONAWI8Oq4rtgO22ZcWnx'

# Kafka settings
KAFKA_TOPIC = 'twitter_stream'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# Twitter API setup
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Kafka producer setup
producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet = {'text': status.text, 'created_at': str(status.created_at)}
        producer.send(KAFKA_TOPIC, value=tweet)

    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

# Stream tweets containing the keyword 'example'
stream.filter(track=['example'])
