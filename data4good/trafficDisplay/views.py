from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    return render(request, "index.html")

def showStats(request):
    return render(request, "tilly.html")

def calculateRiskPage(request):
    return render(request, "calculate.html")