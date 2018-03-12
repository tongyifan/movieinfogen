import re

import requests
import json

from bs4 import BeautifulSoup
from django.db import models


# Create your models here.
def torrentname_format(torrent_name):
    if '].' in torrent_name:
        title = torrent_name[torrent_name.find('].') + 2:torrent_name.find('.torrent')]
    elif '] ' in torrent_name:
        title = torrent_name[torrent_name.find('] ') + 2:torrent_name.find('.torrent')]
    elif '[neubt]' in torrent_name:
        title = torrent_name[torrent_name.find('[neubt]') + 7:torrent_name.find('.torrent')]
    else:
        title = torrent_name[torrent_name.find('fakepath\\') + 9:torrent_name.find('.torrent')]
    if ".mp4" in title:
        title = title[:title.find(".mp4")]
    return title


def gen(torrent_name):
    title = torrentname_format(torrent_name)
    t = re.findall(r'[12][90][0-9][0-9]', title)
    if len(t) == 0:
        return -1
    r = requests.get("http://api.douban.com/v2/movie/search?q=" + title[0:title.find(t[len(t) - 1]) - 1])
    search_json = json.loads(r.text)
    if search_json['total'] == 0:
        return -1
    elif search_json['total'] == 1:
        subject = search_json['subjects'][0]['id']
    else:
        for subjects in search_json['subjects']:
            if subjects['year'] == t[len(t) - 1]:
                subject = subjects['id']

    movieinfogen_api = "https://api.rhilip.info/tool/movieinfo/gen"
    douban_baseurl = "https://movie.douban.com/subject/"
    data = {'url': douban_baseurl + subject}
    r = requests.post(movieinfogen_api, data)
    movie_info = r.json()
    movie_info['poster'] = _extract_poster(movie_info['imdb_link'])
    # todo:将图片传至图床，并在数据库中记录图床中图片编号，与imdb/douban编号一一对应，当数据库中有相应电影海报时直接回报图床链接，提高速度
    movie_info['ename'] = title
    if movie_info['success']:
        return movie_info


def _extract_poster(imdb_link):
    response = requests.get("http://www.imdb.com/title/tt3843282/")
    page = BeautifulSoup(response.text, "html5lib")
    img_url = page.find('div', {'class', 'poster'}).find('a').get("href")
    tt = img_url[img_url.find('tt'):img_url.find('/media')]
    rm = img_url[img_url.find('rm'):img_url.find('?')]
    img_res = requests.get("http://www.imdb.com" + img_url)
    img = BeautifulSoup(img_res.text, "html5lib").find('script').text.strip().replace("'", "\"")
    img_json = json.loads(img[img.find('.push(') + 6:len(img) - 2])
    for image in img_json['mediaviewer']['galleries'][tt]['allImages']:
        if image['id'] == rm:
            return image['src']
    return -1
