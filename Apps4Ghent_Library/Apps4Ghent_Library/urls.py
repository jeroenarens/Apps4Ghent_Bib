from django.conf.urls import patterns, include, url
from django.contrib import admin

from apps4ghent import views

# Register resources

urlpatterns = patterns('',
    # General urls
    url(r'^$', views.index, name='index'),
    url(r'^overview/', views.overview, name='overview'),
    url(r'^leaflet/', views.leaflet, name='leaflet'),
    url(r'^highmap/', views.highmap, name='highmap'),
    url(r'^openlayers/', views.openlayers, name='openlayers'),
    
    # Admin section
    url(r'^admin/', include(admin.site.urls)),
    
    # Api section
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
