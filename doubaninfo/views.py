from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from doubaninfo.models import generate


def hello(request):
    return HttpResponse("Hello world ! ")


def getmovieinfo(request):
    response = JsonResponse(generate(request.GET.get('n')))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
