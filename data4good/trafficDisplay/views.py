from django.shortcuts import render
<<<<<<< HEAD
from django.template import loader
from TrafficAccidents.calculatePlots import myCoolFunc
=======
from trafficAccidents.calculatePlots import myCoolFunc
>>>>>>> d38d13d8e0f20f379379e6a38be987ad6c90a279

def index(request):
    return render(request, "index.html")

def calculateRiskPage(request):
    return render(request, "calculate.html")

def showStats(request):
    context = myCoolFunc
    return render(request, "tilly.html", context)

