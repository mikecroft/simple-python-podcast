import requests
import datetime
from bs4 import BeautifulSoup
from rfeed import *


def processDate(datestring):
    fields = datestring.split()
    day = fields[0][:-2]
    month = fields[1][:3]
    year = fields[2]

    strdate = f'{day}-{month}-{year}'

    return datetime.datetime.strptime(strdate, '%d-%b-%Y')

URL = 'https://www.allsaintsworcester.org.uk/talks'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
talks = soup.find_all('div', class_='sqs-audio-embed')
items = []

for talk in talks:
    dateSpeaker = talk['data-author'].split(" - ")
    date = processDate(dateSpeaker[0])
    speaker = "None" if len(dateSpeaker) < 2 else dateSpeaker[1] 
    url = talk['data-url']

    items.append(Item(
        title = talk['data-title'],
        link = talk['data-url'],
        description = "",
        author = speaker,
        pubDate = date
    ))

feed = Feed(
        title = "talks cast",
        link = "https://www.allsaintsworcester.org.uk/talks",
        description = "",
        language = "en-GB",
        lastBuildDate = datetime.datetime.now(),
        items = items)
 
print(feed.rss())

# https://podgen.readthedocs.io/en/latest/
# https://podba.se/validate/#