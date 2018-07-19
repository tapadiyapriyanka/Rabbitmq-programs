import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',                #exchange is created with name = logs
                         exchange_type='fanout')         #exchange type is defined fanout which mean producer send messages to all lisning consumers

result = channel.queue_declare(exclusive=True)  # when cunsumer connection is closed queue will be exhusted. by option exclusive=True 
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)         # Bind to queue and exchange

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
