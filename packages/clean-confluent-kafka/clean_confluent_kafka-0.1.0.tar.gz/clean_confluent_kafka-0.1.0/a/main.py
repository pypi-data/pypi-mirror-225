from clean_confluent_kafka import KafkaBroker

broker = KafkaBroker(consumer_groups="test2")

print(broker.export_configs())

message = broker.consume()
print(message.value())

message = broker.consume()
print(message.value())
