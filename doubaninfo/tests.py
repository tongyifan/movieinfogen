import json
import configparser
import pymysql
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.test import TestCase

# Create your tests here.
from doubaninfo.models import _extract_poster

print(_extract_poster('tt1365519'))
