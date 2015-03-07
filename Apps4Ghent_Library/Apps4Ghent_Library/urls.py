from django.conf.urls import patterns, include, url
from django.contrib import admin

from apps4ghent import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^items/$', views.ItemList.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
