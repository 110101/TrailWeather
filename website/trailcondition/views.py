from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from algo import run_algo

# Create your views here.
# index view
def index(request):
    # loading the django template
    template = loader.get_template('trailcondition/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

# result view
def result(request):
    template = loader.get_template('trailcondition/result.html')

    # get lat, lon from input form passed when "select" button was clicked
    lat = str(request.POST.get('lat', None))
    lon = str(request.POST.get('lon', None))

    # get weather data and calc results
    #result = run_algo.test(lat, lon)  # for testing
    result = run_algo.get_weather_data(lat, lon)

    # pass to display results on website
    html = {"time_since_rain_days": result["time_since_rain_days"], "time_since_rain_hours": result["time_since_rain_hours"], "lastrain_duration_h": result["lastrain_duration_h"], "rain_status": result["rain_status"], "lastrain_intensity_mm": result["lastrain_intensity_mm"], "rain_commulated_l5days_mm": result["rain_commulated_l5days_mm"], "cos_road": result["cos_road"], "cos_gravel": result["cos_gravel"], "cos_trail": result["cos_trail"], "lat": result["lat"], "lng": result["lon"]}
    return HttpResponse(template.render(html, request))
    # input_result = get_object_or_404(pk=input_lat_lon)
    # input_lat_lon = request.POST.get('input', False)


