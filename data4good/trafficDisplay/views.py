from django.shortcuts import render
from TrafficAccidents.calculatePlots import myCoolFunc

def index(request):
    return render(request, "index.html")

def calculateRiskPage(request):
    return render(request, "calculate.html")

def showStats(request):
    context = myCoolFunc()
    return render(request, "tilly.html", context)

