from django.shortcuts import render
from django.template import loader
from TrafficAccidents.calculatePlots import myCoolFunc

def index(request):
    return render(request, "index.html")

def calculateRiskPage(request):
    context = {
        "score" : 78,
        "recommendation" : "Do not drive"
    }
    return render(request, "calculate.html", context)

def showStats(request):
    plots = myCoolFunc()
    context = {
        "plots" : plots
    }
    return render(request, "explainingDataset.html", context)



# context = {
#     "plots" : {
#         "plot1" : plot1
#         "plot2" : plot1
#         "plot3" : plot1
#         "plot4" : plot1
#     }
# }