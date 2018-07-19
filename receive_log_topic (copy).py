import pika
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

loan_data = pd.read_csv("loan.csv")
sample_data = loan_data[['Loan_ID']].head()

for i in sample_data['Loan_ID']:
    binding_keys = i
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_keys]...\n" % sys.argv[0])
        sys.exit(1)

# for binding_key in binding_keys:
    print("binding_keys = ",binding_keys)
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_keys)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
