import json
import configparser
import pymysql
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.test import TestCase

# Create your tests here.
from doubaninfo.models import _extract_poster, gen

print(gen("[TJUPT].Suicide.squad.2016.1080p.HC.HDTV.x264.AAC-SS (2).torrent"))
