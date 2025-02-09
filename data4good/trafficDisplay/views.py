from django.shortcuts import render
from django.template import loader
from TrafficAccidents.calculatePlots import getPlots
import TrafficAccidents.filterData as filt
from incidence.incidence import find_incidence, get_location
from TrafficAccidents.impact_score_impl import fetch_data

def index(request):
    context = getPlots()
    return render(request, "index.html", context)

def calculateRiskPage(request):
    df = filt.filter_data()
    temp_df = df[~df['prim_contributory_cause'].isin(['NOT APPLICABLE', 'UNABLE TO DETERMINE'])]
    top_10_causes = temp_df['prim_contributory_cause'].value_counts().index[:10][0].lower()
    
    overallScore = 57
    if(overallScore<=100 and overallScore>=70): shouldDrive = "Please do not drive."
    elif(overallScore<70 and overallScore>=30): shouldDrive = "You may be at a higher risk by driving so be careful."
    else: shouldDrive = "You are safe to drive."

    # Get James's Number
    cenlat, cenlon = get_location()
    likelihoodScore = find_incidence(cenlat, cenlon)


    weather_condition = 'Snowing'
    hour = 13
    latitude = 51.340907

    # Get David's numbers
    davidScores = fetch_data(weather_condition, hour, latitude)
    #Baseline is one
    # Do something to make this more pretty
    davidScores[0] = (1 - davidScores[0]) *-100 
    davidScores[0] = ("{:.1f}".format(round(davidScores[0], 2)))

    davidScores[1] = (1 - davidScores[1]) *-100
    davidScores[1] = ("{:.1f}".format(round(davidScores[1], 2)))

    davidScores[2] = (1 - davidScores[2]) *-100
    davidScores[2] = ("{:.1f}".format(round(davidScores[2], 2)))
    # currently thinking displayed as '2x more likely' and '1x less likely'

    # Calculate overall
    # overall = davidScores[0] *  davidScores[1] * davidScores[2] * likelihoodScore

    context = {
        "overallScore" : overallScore,
        "slightScore" : davidScores[0],
        "seriousScore" : davidScores[1],
        "fatalScore" : davidScores[2],
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

def calculationExplain(request):
    return render(request, "calcExplain.html")