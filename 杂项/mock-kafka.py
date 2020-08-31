from gevent import pool
from gevent import monkey; monkey.patch_all()

from kafka import KafkaClient, KafkaProducer, KafkaConsumer
import time
import json
import base64


KAFKA_CLUSTER_SERVERS = [
    '10.10.25.50:19092', 
    '10.10.25.51:19092',
    '10.10.25.52:19092',
    '10.10.25.53:19092',
    '10.10.25.54:19092',
]

topic = "topic.itom.metric.mobile"

# client
client = KafkaClient(KAFKA_CLUSTER_SERVERS)
client.ensure_topic_exists(topic)
# producer
producer = KafkaProducer(bootstrap_servers=KAFKA_CLUSTER_SERVERS)

def f(num):
	taskid = "taskid{num}".format(num=num)
	version = "version{num}".format(num=num)
	# send message to kafka
	producer.send(topic, json.dumps(
	{
		"https": [
			{"taskId": taskid, "appVersion": version, "errorId": 500, "responseTime": 1},
			{"taskId": taskid, "appVersion": version, "errorId": 5, "responseTime": 1}
		]
	}
	))

############################
# config
total_count = 1000
batch_count = 100
interval_time = 3
gevent_pool_num = 20
############################

print("mock total_count: %d, batch_count: %d start" % (total_count, batch_count))
p = pool.Pool(gevent_pool_num)
batch = 1
while 1:
    time.sleep(interval_time)
	# send M message every Ns
	p.map(f, map(lambda i: "-%d-%d" % (batch, i+1), range(batch_count)) )
	print("mock total_count: %d, batch: %d ok" % (total_count, batch))
	# stop
	if batch*batch_count >= total_count:
		break
	batch += 1
producer.close()
print("mock total_count: %d, batch: %d all end" % (total_count, batch))


"""
# consumer
print('start consuming...')
consumer = KafkaConsumer(topic, group_id=topic+"_group", bootstrap_servers=KAFKA_CLUSTER_SERVERS)
count = 0
for msg in consumer:	
    print("consume 1 mesg from %s:%d:%d: k=%s" % (msg.topic, msg.partition, msg.offset, msg.key))
    print(json.loads(msg.value))
	count += 1
"""


