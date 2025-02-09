from django.shortcuts import render
from django.template import loader
from TrafficAccidents.calculatePlots import getPlots
import TrafficAccidents.filterData as filt
from incidence.incidence import find_incidence, get_location

def index(request):
    return render(request, "index.html")

def calculateRiskPage(request):
    df = filt.filter_data()
    temp_df = df[~df['prim_contributory_cause'].isin(['NOT APPLICABLE', 'UNABLE TO DETERMINE'])]
    top_10_causes = temp_df['prim_contributory_cause'].value_counts().index[:10][0].lower()
    overallScore = 57
    if(overallScore<=100 and overallScore>=70): shouldDrive = "Please do not drive."
    elif(overallScore<70 and overallScore>=30): shouldDrive = "You may be at a higher risk by driving so be careful."
    else: shouldDrive = "You are safe to drive."


    cenlat, cenlon = get_location()
    likelihoodScore = find_incidence(cenlat, cenlon)


    context = {
        "overallScore" : 57,
        "slightScore" : 21,
        "seriousScore" : 92,
        "fatalScore" : 82,
        "likelihoodScore" : likelihoodScore,
        "recommendation" : f"{shouldDrive} Most people make mistakes by {top_10_causes}."
    }
    return render(request, "calculate.html", context)

def showStats(request):
    plots = getPlots()
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