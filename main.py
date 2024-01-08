import schedule
import time
import os
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

password = os.environ['mailPass']
username = os.environ['mailUsername']

myPrice = 300.0

def getPrice():
  url = "https://www.zalando.lv/cras-pariscras-boots-zabaki-silver-crg11a000-d11.html"
  response = requests.get(url)
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')
  price_span = soup.find('span', {'class': 'sDq_FX _4sa1cA FxZV-M HlZ_Tf'})  
  
  if price_span:
      price = price_span.text.strip()
      return price , url
  else:
      print('Price not found.')
      return 0.0
    

def sendEmail(price_str, link):

    server = "smtp.gmail.com"
    port = 587
    s = smtplib.SMTP(host=server, port=port)
    s.starttls()
    s.login(username, password)

    msg = MIMEMultipart()
    msg['To'] = "marinamoger@yahoo.com"
    msg['From'] = username
    msg['Subject'] = f"The price has dropped to {price_str} !\n Link: {link}"
    s.send_message(msg)
    del msg

def printMe():
    price, link = getPrice()
    price_str = price.replace('\xa0', '').replace(',', '.')
    price_float = float(''.join(char for char in price_str if char.isdigit() or char in {',', '.'}))

    if price_float != 0.0 and price_float < myPrice:
      print("⏰ Sending a reminder")
      sendEmail(price_str, link)

schedule.every(2).hours.do(printMe)

while True:
    schedule.run_pending()
    time.sleep(1)
