import asyncio
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from azure.servicebus.aio import ServiceBusClient

CONNECTION_STR = os.environ['SERVICEBUS_CONNECTION_STR']
QUEUE_NAME = os.environ["SERVICEBUS_QUEUE_NAME"]

async def run(loop,logger=None):
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)
    while True:
        print("waiting message...")
        async with servicebus_client:
            receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME)
            async with receiver:
                received_msgs = await receiver.receive_messages(max_message_count=10, max_wait_time=1)
                for msg in received_msgs:
                    mail = {}
                    try:
                        mail = json.loads(str(msg))
                    except:
                        print(str(msg))
                        continue;
                    print(str(mail))
                    asyncio.create_task(send_email(mail))
                    await receiver.complete_message(msg)

async def send_email(mail):
    try:
        async with aiosmtplib.SMTP(hostname=mail["smtp"]["server"], port=mail["smtp"]["port"]) as smtp:
            email = MIMEMultipart('alternative')
            email["From"] = mail['sender']
            email["To"] = mail['receiver']
            if('bcc' in mail and mail['bcc']):
                email["BCC"] = mail['bcc']
            if('cc' in mail and mail['cc']):
                email["CC"] = mail['cc']
            email["Subject"] = mail['subject']
            email.attach(MIMEText(mail['message'], "html"))
            await aiosmtplib.send(email, hostname=mail["smtp"]["server"], port=mail["smtp"]["port"],username=mail["smtp"]["username"],password=mail["smtp"]["password"])

    except Exception as e:
        print("Error:", e)