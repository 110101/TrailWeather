from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from algo import run_algo

# Create your views here.
def index(request):
    # loading the django template
    template = loader.get_template('trailcondition/index.html')
    context = {}
    return HttpResponse(template.render(context, request))
    #return render(request, 'index.html', context)

def result(request):
    template = loader.get_template('trailcondition/result.html')
    lat = str(request.POST.get('lat', None))
    lon = str(request.POST.get('lon', None))
    # result = run_algo.get_weather_data(lat, lon)
    result = run_algo.test(lat, lon)
    html = {"time_since_rain_h": str(result["time_since_rain_h"]), "lastrain_duration_h": str(result["lastrain_duration_h"]), "rain_status": str(result["rain_status"]), "lastrain_intensity_mm": str(result["lastrain_intensity_mm"]), "lat": str(result["lat"]), "lng": str(result["lng"])}
    return HttpResponse(template.render(html, request))
    # input_result = get_object_or_404(pk=input_lat_lon)
    # input_lat_lon = request.POST.get('input', False)


