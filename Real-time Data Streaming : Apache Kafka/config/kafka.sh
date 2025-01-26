# start zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# start kafka brokers (Servers = cluster)
bin/kafka-server-start.sh config/server.properties

# create a topic
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

# list all topic
bin/kafka-topics.sh --list --zookeeper localhost:2181

# configure brokers to auto-create topics when a non-existent topic is published to

# see topic details (partition, replication factor)
bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic test

# change partition number of a topic --alter
# Note: While Kafka allows us to add more partitions, it is NOT possible to decrease number of partitions of a Topic. 
# In order to achieve this, you need to delete and re-create your Topic.
bin/kafka-topics.sh --alter --zookeeper localhost:2181 --topic test --partitions 3

# PRODUCER -----------------------------------
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test

# CONSUMER -----------
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic test
# removed --from-beginning => consumer only gets message that is produced after it is up
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test

#Kafka CONNECT-----------------------------
# 2 stand-alone connectors (run in a single,local,dedicated process)
bin/connect-standalone.sh \ 
  config/connect-standalone.properties \
  config/connect-file-source.properties \
  config/connect-file-sink.properties

