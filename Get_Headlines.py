import xml.etree.ElementTree as ET
import requests

# source URL
google_news_url = "https://news.google.com/news/rss"

# this function will get the headlines from RSS feed 
def get_headlines(rss_url):
    # creating an empty list to store the headlines
    titles = []

    response = requests.get(rss_url)
    # making sure our request returned the necessary info 
    if response.status_code == 200:
        # Creating an Element Tree from our XML document
        root = ET.fromstring(response.content)
        # iterating over all the tags and retrieving the necessary data
        for item in root.findall('.//item'):
            title = item.find('title').text
            titles.append(title)
        return titles
    else:
        print(f"Error code {response.status_code}, unable to connect")

