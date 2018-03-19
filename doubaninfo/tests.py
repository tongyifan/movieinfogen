import json
import configparser
import pymysql
import requests
import time
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.test import TestCase

# Create your tests here.
from doubaninfo.models import generate
# print(generate('file:///home/tongyifan/Downloads/[BYRBT].无人区.No.Man\'s.Land.2013.BluRay.1080p.x265.MNHD-FRDS.torrent'))
# print(generate('file:///home/tongyifan/Downloads/[BYRBT].怦然心动.Flipped.2010.BluRay.1080p.x265.10bit.2Audio.MNHD-FRDS.torrent'))
# print(generate("file:///home/tongyifan/Downloads/[BYRBT].Blind.Chance.1987.720p.BluRay.FLAC2.0.x264-Przypadek.torrent"))
# print(generate("file:///home/tongyifan/Downloads/[BYRBT].The.Killing.of.a.Sacred.Deer.2017.720p.BluRay.DD5.1.x264-BMF.mkv.torrent"))
# print(generate("file:///home/tongyifan/Downloads/[TJUPT].Downsizing.2017.720p.BluRay.x264-WiKi.torrent"))
# print(generate("file:///home/tongyifan/Downloads/[TJUPT].Twenty.Two.2015.WEB-DL.4K.H264.AAC-TJUPT.mp4.torrent"))
# print(_extract_poster_douban(27140017, "https://img1.doubanio.com/view/photo/l_ratio_poster/public/p2510604929.jpg"))