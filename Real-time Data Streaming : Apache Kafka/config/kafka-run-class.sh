#run Java class

# ConsumerOffsetCheck. run when Kafka server is up, there is a topic + messages produced and consumed
bin/kafka-run-class.sh kafka.tools.ConsumerOffsetChecker --broker-info --zookeeper localhost:2181 --group test-consumer-group
# ConsumerOffsetChecker has been removed in Kafka 1.0.0. Use kafka-consumer-groups.sh to get consumer group details
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group consule-consumer-38063
  # bootstrap-server=kafka broker server to connect to, NOT zookeeper
  # --describe => describe consumer group and list offset lag (# messages not yet processed)

# get a list of active consumer groups in cluster
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

#get latest offset
bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic test --time -1 --offsets 1

# offset of last available message in topic's partition --time -1
bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic test --time -1

# offset of first available message in topic's partition --time -2
bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic test --time -2


