import os
from twilio.rest import Client
from dotenv import load_dotenv
from scraper import requestGME
from scraper import get_proxies

load_dotenv()

account_sid = os.getenv('ACCOUNT')
auth_token = os.getenv('TOKEN')

client = Client(account_sid, auth_token)


proxies = get_proxies()
availability = requestGME(proxies)

if availability == 'Available':
    message = client.messages.create (
        to = os.getenv('RECIPIENT'),
        from_= os.getenv('SENDER'),
        body = "The playstation 5 is in stock now at Gamestop.com"
    )