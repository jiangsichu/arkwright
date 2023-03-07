import os
import scrapy
import smtplib
from email.mime.text import MIMEText

MAIL_FROM = os.environ.get('MAIL_FROM')
MAIL_PWD = os.environ.get('MAIL_PWD')
MAIL_TO = os.environ.get('MAIL_TO')
SEEKED_HOUSE = os.environ.get('SEEKED_HOUSE')

def send_mail(subject, body):
    msg = MIMEText(body or '')
    msg['Subject'] = subject
    msg['From'] = MAIL_FROM
    msg['To'] = ', '.join(MAIL_TO)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(MAIL_FROM, MAIL_PWD)
    smtp_server.sendmail(MAIL_FROM, MAIL_TO, msg.as_string())
    smtp_server.quit()

class HousesSpider(scrapy.Spider):
    name = "houses"
    start_urls = ["https://www.bellway.co.uk/new-homes/kent/alkerden-heights"]
        
    def parse(self, response):
        for house in response.css('div#house-styles article'):
            title = house.css('span.result-title::text').get()
            price = house.css('span.result-pricing strong::text').get()
            self.logger.debug('House type: %s, price: %s', title, price)
            
            if title == SEEKED_HOUSE:
                self.logger.info('Sending email for house: %s, price: %s', title, price)
                send_mail(subject=title, body=price)

            yield {
                'title': title,
                'price': price,
            }
