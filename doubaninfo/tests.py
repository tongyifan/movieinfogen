import json

import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.test import TestCase

# Create your tests here.

#response = requests.get("https://images-na.ssl-images-amazon.com/images/M/MV5BYWZjNWI5OTYtZDEwYy00YTY5LTllNGMtYzJiMDNmOTM3NGY1XkEyXkFqcGdeQXVyNjc2MDYyODM@._V1_SY1000_CR0,0,714,1000_AL_.jpg")
#fl = open('1.jpg', 'rb').read()
#files = {'smfile': ('test.jpg', fl, 'image/jpeg')}
#print(files)
#smfile = requests.post("https://sm.ms/api/upload", files)
#print(smfile.text)
from doubaninfo.models import gen

print(JsonResponse(gen('C:\\fakepath\\[TJUPT].The.Ex-FileThe.Return.of.the.Exes.2017.WEB-DL.4K.H264.AAC-TJUPT.mp4.torrent')))