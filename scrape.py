import requests
import datetime
from bs4 import BeautifulSoup
from podgen import Podcast, Episode, Media

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

p = Podcast(
   name="ASW Talks",
   description="Talks from ASW.",
   website=URL,
   explicit=False,
)
items = []

for talk in talks:
    dateSpeaker = talk['data-author'].split(" - ")
    date = processDate(dateSpeaker[0])
    speaker = "None" if len(dateSpeaker) < 2 else dateSpeaker[1] 
    if (talk['data-url'] == ""):
        continue
    else:
        items.append(Episode(
            title = talk['data-title'],
            media = Media(
                url = talk['data-url']
                ),
            summary = f'A talk from ASW by {speaker} on {date}'
            # author = speaker,
            # pubDate = date
        ))

# Add some episodes
p.episodes = items
# Generate the RSS feed
rss = p.rss_str()

print(rss)