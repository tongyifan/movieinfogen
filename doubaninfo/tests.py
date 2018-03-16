import json
import configparser
import pymysql
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.test import TestCase

# Create your tests here.
from doubaninfo.models import _extract_poster, gen

print(gen("C:\\fakepath\\[TJUPT].Fight.Club.1999.BluRay.720p.x264.DTS-WiKi.torrent"))
