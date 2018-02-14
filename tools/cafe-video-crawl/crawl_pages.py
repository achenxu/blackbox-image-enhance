import os
import time
import sys
import copy
import requests
import json
import shutil
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from bs4 import BeautifulSoup


# arguments from environments
# CAFE_LOGIN_PAGE - login page URL
# CAFE_ID - user id
# CAFE_PW - user password
# CAFE_BASE_URL - cafe base url
# VIDEO_INFO_API_URL - video info url

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')

# hide headless mode
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

# chrome_options=options)
driver = webdriver.Chrome('/Applications/chromedriver', chrome_options=options)

cafe_base = os.environ['CAFE_BASE_URL']
info_api = os.environ['VIDEO_INFO_API_URL']


def naver_login():
    driver.get(os.environ['CAFE_LOING_PAGE'])
    driver.find_element_by_name('id').send_keys(os.environ['CAFE_ID'])
    driver.find_element_by_name('pw').send_keys(os.environ['CAFE_PW'])
    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input')\
        .click()


def save_article(num):
    driver.get('%s/%d' % (cafe_base, num))

    try:
        driver.switch_to.alert.accept()
    except NoAlertPresentException:
        cafe_main = driver.find_element_by_css_selector('iframe#cafe_main')
        driver.switch_to_frame(cafe_main)
        buf = copy.copy(driver.page_source)
        with open("data_html/%d.html" % num, "w") as f:
            f.write(driver.page_source)
            driver.switch_to_default_content()
        print("Save Page %d" % num)
        return buf
    else:
        print("No Page %d" % num)
        return None


def find_image_url(num, buf):
    soup = BeautifulSoup(buf, 'html.parser')
    mplayers = soup.select('iframe[name="mplayer"]')
    result = []
    if len(mplayers) > 0:
        print("  Found %d movies" % len(mplayers))
        for x in mplayers:
            urls = urlparse(x['src'])
            qs = parse_qs(urls.query)
            result.append({'videoId': qs['vid'][0], 'inKey': qs['inKey'][0]})
    return result


def get_image_json(num, idx, qs):
    r = requests.get(info_api, qs)

    name = "data_json/%d-%d.json" % (num, idx)
    with open(name, "w") as f:
        f.write(r.text)
    j = json.loads(r.text)
    videos = j['videos']['list']
    seq = [float(x['bitrate']['video']) for x in videos]
    max_value = max(seq)
    data = [(i, val) for (i, val) in enumerate(videos)
            if float(val['bitrate']['video']) == max_value]
    return data[0][1]


if __name__ == '__main__':
    naver_login()
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    step = 1 if start < end else -1
    for i in range(start, end, step):
        html = save_article(i)
        if not html:
            continue

        imgs_info = find_image_url(i, html)
        if len(imgs_info) <= 0:
            continue

        for idx, qs in enumerate(imgs_info):
            data = get_image_json(i, idx, qs)
            print('  Download %s' % data['source'])
            r = requests.get(data['source'], stream=True)
            if r.status_code == 200:
                print('  Saved data_mp4/%d-%d.mp4' % (i, idx))
                with open('data_mp4/%d-%d.mp4' % (i, idx), 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

        time.sleep(1)

    driver.quit()
