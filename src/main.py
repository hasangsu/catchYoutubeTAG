import sys
import re
import requests
from bs4 import BeautifulSoup

# check url is youtube?
def is_youtube_link(url):
    youtube_regex = re.compile(
    r'(https?://)?(www\.)?'
    r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
    r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    return re.match(youtube_regex, url) is not None

# check sys argv count
if len(sys.argv) != 2 :
    print("the argv count is invalid.")
    sys.exit()

# check youtube url
url = sys.argv[1]
result = is_youtube_link(url)
if not result :
    print("url is not youtube url.")
    sys.exit()
    
# .get() is sends a GET request
# return is server’s response to an HTTP request
# if the response code is 200 OK
response = requests.get(url)
if not response.ok:
    print("fail request.")
    sys.exit()

# get url html
soup = BeautifulSoup(response.text, 'html.parser')

# get movie title in url html
# title = soup.select_one('meta[property="og:title"]')['content']
title = soup.select_one('meta', property='og:title')['content']

# get movie hash tag in url html (TBD)

# get movie tag in url html
meta_tags = soup.find_all('meta', property="og:video:tag")
contnt_tags = [tag['content'] for tag in meta_tags]
tags = ', '.join(contnt_tags)

# print parse result
print(title)
print(tags)