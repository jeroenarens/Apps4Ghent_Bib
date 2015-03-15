from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework_mongoengine.routers import MongoDefaultRouter

from apps4ghent import views

# Register resources
router = MongoDefaultRouter()
router.register(r'items', views.ItemsViewSet)
router.register(r'item-copies', views.ItemCopyViewSet)
router.register(r'borrowers', views.BorrowerViewSet)
router.register(r'borrowings', views.BorrowingViewSet)
router.register(r'reservations', views.ReservationViewSet)

urlpatterns = patterns('',
    # General urls
    url(r'^$', views.index, name='index'),
    
    # Admin section
    url(r'^admin/', include(admin.site.urls)),
    
    # Api section
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
