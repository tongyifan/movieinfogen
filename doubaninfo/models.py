import configparser
import re

import pymysql
import requests
import json

from bs4 import BeautifulSoup
from django.db import models


# Create your models here.

def err(code, msg):
    error = {'errcode': code, 'msg': msg}
    return error


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
    if '1080' in t:
        t.remove('1080')
    if len(t) == 0:
        return err("-999", "暂时无法解析，目前的解析策略必须使用正式的0day名")
    r = requests.get("http://api.douban.com/v2/movie/search?q=" + title[0:title.find(t[len(t) - 1]) - 1])
    search_json = json.loads(r.text)
    if search_json['total'] == 0:
        return err(-1, "搜索结果为空")
    elif search_json['total'] == 1:
        subject = search_json['subjects'][0]['id']
    else:
        for subjects in search_json['subjects']:
            if subjects['year'] == t[len(t) - 1]:
                subject = subjects['id']
    if 'subject' not in locals().keys():
        return err(-1, "搜索结果为空")
    movieinfogen_api = "https://api.rhilip.info/tool/movieinfo/gen"
    douban_baseurl = "https://movie.douban.com/subject/"
    data = {'url': douban_baseurl + subject}
    r = requests.post(movieinfogen_api, data)
    movie_info = r.json()
    if movie_info['success']:
        poster = _extract_poster(movie_info['imdb_id'])
        if poster != 1:
            movie_info['poster'] = _extract_poster(movie_info['imdb_id'])
            movie_info['format'] = '[img]' + movie_info['poster'] + '[/img]\n' + movie_info['format']
        movie_info['ename'] = title
        return movie_info
    return err(-1, "API回报错误")


def _extract_poster(imdb_id):
    config = configparser.ConfigParser()
    config.read('pymysql.ini')
    db = pymysql.connect(config.get('movieposter', 'Hostname'), config.get('movieposter', 'Username'),
                         config.get('movieposter', 'Password'), 'movieposter')
    cursor = db.cursor()
    cursor.execute('SELECT img_link FROM imdbimg WHERE imdb_id = %s', imdb_id)
    result = cursor.fetchone()
    if result is None:
        response = requests.get("http://www.imdb.com/title/" + imdb_id)
        page = BeautifulSoup(response.text, "html5lib")
        try:
            img_url = page.find('div', {'class', 'poster'}).find('a').get("href")
        except:
            return 1
        tt = img_url[img_url.find('tt'):img_url.find('/media')]
        rm = img_url[img_url.find('rm'):img_url.find('?')]
        img_res = requests.get("http://www.imdb.com" + img_url)
        img = BeautifulSoup(img_res.text, "html5lib").find('script').text.strip().replace("'mediaviewer'",
                                                                                          "\"mediaviewer\"")
        img_json = json.loads(img[img.find('.push(') + 6:len(img) - 2])
        for image in img_json['mediaviewer']['galleries'][tt]['allImages']:
            if image['id'] == rm:
                url = image['src']
                headers = {"user-agent": "Mozilla/5.0"}
                response = requests.get(url=url, headers=headers)
                files = {'smfile': ('poster.jpg', response.content, 'image/jpeg')}
                smresponse = requests.post(url="https://sm.ms/api/upload", files=files).json()
                if smresponse['code'] == "success":
                    sql = 'INSERT INTO imdbimg(imdb_id, img_link, del_link) VALUES (%s, %s, %s)'
                    try:
                        cursor.execute(sql, [imdb_id, smresponse['data']['url'], smresponse['data']['delete']])
                        db.commit()
                    except:
                        db.rollback()
                return smresponse['data']['url']
        return err(-2, "获取海报失败")
    else:
        return result[0]
