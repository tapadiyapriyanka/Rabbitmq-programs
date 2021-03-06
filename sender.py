import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
print("connection created by sender")

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
                      
print("channel published by sender")
print(" [x] Sent 'Hello World!'")
connection.close()