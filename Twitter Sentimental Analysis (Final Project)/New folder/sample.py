import tweepy

# Twitter API credentials
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHy%2FugEAAAAASuKZiULDBj65SEbXkqav6a8Fa7A%3DHjCzCYt5MoMdpUqgwG8cEqwtIqAskGFnWeOY56bUYFQXkiGnyo'

# Verify credentials
client = tweepy.Client(bearer_token)
user = client.get_user(username='faiq_latheef')
print(user)
