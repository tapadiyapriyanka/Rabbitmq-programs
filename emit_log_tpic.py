import pika
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')
                         
loan_data = pd.read_csv("loan.csv")
sample_data = loan_data[['Loan_ID', 'ApplicantIncome']].head()
a = sample_data['Loan_ID']
for i in a:
    print(i)
    routing_key = i
    # routing_key = 'LP001002'
    message = sample_data.loc[sample_data['Loan_ID'] == routing_key, 'ApplicantIncome'].iloc[0]
    
    # message = sample_data.loc[sample_data['Loan_ID'] == i, 'ApplicantIncome'].item()
    # message = sample_data[sample_data['Loan_ID']==i]['ApplicantIncome']
    # message = "hello"
    print("message = ",message)
    channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=str(message))
    print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()