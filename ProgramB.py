import pika
import random
import time

## Connect RabbitMQ services
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='numberStoreA') # Declare queue
channel.queue_declare(queue='pointStoreB') # Declare queue

def success(increase):
    if increase == True:
        print("SUCCESSFUL PREDICT\n")
        channel.basic_publish(exchange='',routing_key='pointStoreB',body="1 Point")
    if increase == False:
        print("unsuccessful\n")
    return

def isTrue(body,predictsList):
    # Answer is True or False?
    increase = False
    for n in predictsList:
        if int(n) == int(body):
            increase = True
    success(increase)
    return

def prediction():
    predictsList = []
    for i in range(5):
        predictsList.append(random.randint(0,9))
    quest = random.randint(0,9)
    print("Here are the predicts list: {}".format(predictsList))
    return predictsList, quest

def callback(ch, method, properties, body):
    predictsList, quest = prediction() # Generate numbers

    body = body.decode("utf-8") # Body comes as a byte object
    print("Forecasts receive is {}".format(body))
    isTrue(int(body),list(predictsList)) # Predicts are True or False
    time.sleep(3) # Sleep for read command line on testing

    print("Sending this number: {}".format(quest))

    # Send quest number
    channel.basic_publish(exchange='',routing_key='numberStoreB',body=str(quest))

def listener():
    print('Press CTRL+C to exit to game\nThe game will begin\n')
    ## Listens to programA / on queue='B'
    channel.basic_consume(on_message_callback=callback,queue='numberStoreA')
    channel.start_consuming()

def firstMsg():
    predictsList, quest = prediction()  # Generate numbers
    # Send first quest number
    channel.basic_publish(exchange='',routing_key='numberStoreB',body=str(quest))
    return

if __name__=="__main__":
    firstMsg()
    listener() # Main objective