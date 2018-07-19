import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
print("connection created by receiver..")

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
                      
print("channel consumed by consumer.")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
