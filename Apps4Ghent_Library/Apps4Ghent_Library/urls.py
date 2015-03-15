from django.conf.urls import patterns, include, url
from django.contrib import admin

from apps4ghent import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^items/$', views.ItemList.as_view()),
    url(r'^item-copies/$', views.ItemCopyList.as_view()),
    url(r'^borrowers/$', views.BorrowerList.as_view()),
    url(r'^borrowings/$', views.BorrowingList.as_view()),
    url(r'^reservations/$', views.ReservationList.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
