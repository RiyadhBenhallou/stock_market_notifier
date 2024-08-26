from twilio.rest import Client
import os
import requests
from datetime import datetime, timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
alphavantage_api_key = os.environ['ALPHAVANTAGE_API_KEY']

url = F'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={alphavantage_api_key}'
r = requests.get(url)
data = r.json()

def get_close(day):
  return float(data['Time Series (Daily)'][str(day)]['4. close'])

today = datetime.today().date()
start_day = today - timedelta(days = 3)
before_day = today - timedelta(days = 4)
close_price = get_close(start_day)
close_price_before = get_close(before_day)

def percentage(num1, num2):
  difference = (num1 - num2) / abs(num2) * 100
  return round(difference, 2)

def format_articles(articles):
  formatted_articles = ''
  for article in articles:
    formatted_articles += f"""
      Headline: {article['title']}
      Description: {article['description']}
      
    """
  return formatted_articles


account_sid = os.environ['TWILIO_ACC_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


diff = percentage(close_price, close_price_before)

if diff <= 5 or diff >= 5:
  news_r = requests.get(f'https://newsapi.org/v2/everything?q=Tesla&from={str(start_day)}&sortBy=popularity&apiKey=cba8d512fd864f9695843fe4e78daf59')
  news_data = news_r.json()
  news = news_data['articles'][:3]
  message = client.messages.create(
    from_='+12568260894',
    to='+213541759528',
    body= f"""
      {COMPANY_NAME}: {f'🔺{diff}' if diff > 5 else f'🔻{diff}'}
      {format_articles(news)}
    """
  )
  print(message.sid)
else:
  pass
