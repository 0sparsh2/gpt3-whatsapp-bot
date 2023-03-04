import datetime
import logging
import azure.functions as func

import requests
from twilio.rest import Client
secret_key = "OPEN AI KEY"

import openai
import requests
from bs4 import BeautifulSoup

openai.api_key = secret_key

account_sid = 'GET FROM TWILIO'
auth_token = 'GET FROM TWILIO'
client = Client(account_sid, auth_token)

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    total_output = ""
    # Enter the topics you want to search for
    titles = ["Start Up news", "AI news"] 
    for title in titles:
        links = []
        # Google search URL for the topic
        url = f"https://www.google.com/search?q={title}&tbm=nws&sxsrf=AJOqlzXXEH0G1GhYrC3JkmLJWdloCetKmw:1677891680893&tbas=0&source=lnt&sa=X&ved=2ahUKEwjUxfHMicH9AhWv3TgGHYAtCrUQpwV6BAgBEBQ&biw=1354&bih=630&dpr=1"
        response = requests.get(url)
        # Scrape browser on the topics for article links
        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and "http" in href and ".google." not in href:
                new_link = (href[7:]).split('&sa=U')[0]
                links.append(new_link)
        
        links_str = ", ".join(links)
        
        # Prompt to look up the article content and summarize
        message =   """
                    Go through all the articles in the following links separated by commas, give me a collecive 3 small one liner summary with links :
                    {}
                    """.format(links_str)
        
        links_str = ""

        # Use the code for deploying API of open ai and use here
        openaiurl = 'OPEN AI API THAT YOU CREATED'
        data = {"model":"text-davinci-003", "prompt":message, "temperature":0.6, "max_tokens":300}
        response = requests.get(openaiurl, json=data)
        content = response.content
        result = content.decode('utf8').replace("'",'"')

        output = result + "\n"

        total_output += output

    # You can find exact syntax for this on Twilio docs
    message = client.messages.create(
    from_='whatsapp:NUMBER GIVEN BY TWILIO',
    body= total_output,
    to='whatsapp:YOUR NUMBER'
    )

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
