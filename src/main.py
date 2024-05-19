import sys
import re

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

url = sys.argv[1]
result = is_youtube_link(url)
print(result)
    