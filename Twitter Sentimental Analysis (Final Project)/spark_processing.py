# spark_processing.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType
from textblob import TextBlob
from elasticsearch import Elasticsearch
from datetime import datetime

# Create Spark session
spark = SparkSession.builder \
    .appName("TwitterSentimentAnalysis") \
    .getOrCreate()

# Define schema for incoming data
schema = StructType([
    StructField("text", StringType(), True),
    StructField("created_at", StringType(), True)
])

# Kafka settings
KAFKA_TOPIC = 'twitter_stream'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# Read data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .load()

# Convert the value column to a string
df = df.selectExpr("CAST(value AS STRING)")

# Parse JSON and extract fields
json_df = df.withColumn("value", from_json("value", schema)).select(col("value.*"))

# Define UDF for sentiment analysis
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

sentiment_udf = udf(get_sentiment, StringType())

# Add sentiment column
sentiment_df = json_df.withColumn("sentiment", sentiment_udf(col("text")))

# Write processed data to Elastic Search
def send_to_elastic(df, epoch_id):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    for row in df.collect():
        es.index(index="twitter_sentiment", doc_type="tweet", body={
            "text": row.text,
            "created_at": row.created_at,
            "sentiment": row.sentiment,
            "timestamp": datetime.now()
        })

query = sentiment_df.writeStream \
    .foreachBatch(send_to_elastic) \
    .outputMode("append") \
    .start()

query.awaitTermination()
