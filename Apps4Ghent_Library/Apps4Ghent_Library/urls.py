from django.conf.urls import patterns, include, url
from django.contrib import admin

from apps4ghent import views

urlpatterns = patterns('',
    # General urls
    url(r'^$', views.index, name='index'),
    
    # Admin section
    url(r'^admin/', include(admin.site.urls)),
    
    # Api section
    url(r'^api/v1/items/$', views.ItemList.as_view()),
    url(r'^api/v1/item-copies/$', views.ItemCopyList.as_view()),
    url(r'^api/v1/borrowers/$', views.BorrowerList.as_view()),
    url(r'^api/v1/borrowings/$', views.BorrowingList.as_view()),
    url(r'^api/v1/reservations/$', views.ReservationList.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
