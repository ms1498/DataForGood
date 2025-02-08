from django.shortcuts import render
from django.template import loader

def index(request):
    return render(request, "index.html")

def calculateRiskPage(request):
    return render(request, "calculate.html")

def showStats(request):

    return render(request, "tilly.html")

