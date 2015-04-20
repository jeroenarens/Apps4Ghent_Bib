from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from apps4ghent import views

# Register resources
router = routers.SimpleRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'item-copies', views.ItemCopyViewSet)
router.register(r'sectors', views.SectorViewSet)
router.register(r'borrowers', views.BorrowerViewSet)

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
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
