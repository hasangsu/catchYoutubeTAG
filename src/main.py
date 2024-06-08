import sys
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# check url is youtube?
def is_youtube_link(url):
    youtube_regex = re.compile(
    r'(https?://)?(www\.)?'
    r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
    r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    return re.match(youtube_regex, url) is not None

def check_vaild_youtube():
    # check sys argv count
    if len(sys.argv) != 2 :
        print("the argv count is invalid.")
        return False

    # check youtube url
    url = sys.argv[1]
    result = is_youtube_link(url)
    if not result :
        print("url is not youtube url.")
        return False

    return True

def catch_title(soup):
    title = (soup.find("div", attrs={"id": "title", "class": "ytd-watch-metadata"})).find("yt-formatted-string").text
    return title

def catch_tag(soup):
    meta_tags = soup.find_all('meta', property="og:video:tag")
    contnt_tags = [tag['content'] for tag in meta_tags]
    tag = ', '.join(contnt_tags)
    return tag

def catch_hash_tag(soup):
    expender_contents = soup.find_all("a", class_="yt-core-attributed-string__link--display-type")

    contnt_tags = []
    for content in expender_contents:
        if content.text[0] == "#":
            contnt_tags.append(content.text)
    
    hash_tag = ' '.join(contnt_tags)
    return hash_tag

def run_selenium(target_url):
    # create selenium options
    options = webdriver.ChromeOptions()

    # hide selenium dynamic web page
    options.add_argument("headless")

    # run selenium
    driver = webdriver.Chrome(options=options)
    driver.get(target_url)
    
    # wait web dynamic loading
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "title"))
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "description-text-container"))
    )
    
    return driver

def stop_selenium(driver):
    driver.quit()
    return

def output_catch_information(title, tags, hash_tag):
    green_color = '\033[32m'
    reset_color = '\033[0m'
    
    print(f"{green_color}Catch Information (Title, Tag, Hash Tag){reset_color}")
    print(title)
    print(tags)
    print(hash_tag)
    return

# start main catch youtube
def start_catch_youtube():
    is_valid = check_vaild_youtube()
    if not is_valid :
        sys.exit()
        return
    
    target_url = sys.argv[1]

    # run selenium dynamic web page
    driver = run_selenium(target_url)

    # get url html
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # get movie title in url html
    title = catch_title(soup)

    # get movie tag in url html
    tag = catch_tag(soup)

    # get movie hash tag in url html
    hash_tag = catch_hash_tag(soup)

    # output catch information
    output_catch_information(title, tag, hash_tag)

    stop_selenium(driver)
    return

start_catch_youtube()