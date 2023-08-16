import pika
import requests
from elasticsearch import Elasticsearch
es_host = 'localhost'
es_port = 9200
es = Elasticsearch(hosts=[{'host': es_host, 'port': es_port}])

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='data_queue')
# Callback function to handle incoming messages
def callback(ch, method, properties, body):
    data = eval(body)
 # Create a document
    doc = {
        'title': data['title'],  # Use title as the author for simplicity
        'place': data['place'],    # Use place as the text content
        'price':data['price'],
       'image':data['image_links'],
       'engine-capacity':data['engine'],
       'Registered In':data['registered']
    }

    # Index the document
    resp = es.index(index="pak-string", id=data['count'], body=doc, doc_type="data")
    print(resp)

# Set up a consumer
channel.basic_consume(callback,queue='data_queue',  no_ack=True)

print("Consumer started. Waiting for messages...")
channel.start_consuming()

