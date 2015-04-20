from django.shortcuts import render_to_response

from .serializers import *

def index(request):

   return render_to_response('index2.html')

def overview(request):
    return render_to_response('overview.html')

def leaflet(request):
    return render_to_response('leaflet.html')

def openlayers(request):
    return render_to_response('openlayers.html')

def highmap(request):
    return render_to_response('highmaps.html')

