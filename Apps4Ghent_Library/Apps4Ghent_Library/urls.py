from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from apps4ghent import views

# Register resources
#API endpoint urls (/api/v1/...)
router = routers.SimpleRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'item-copies', views.ItemCopyViewSet)
router.register(r'sectors', views.SectorViewSet)
router.register(r'borrowers', views.BorrowerViewSet)
router.register(r'borrowings', views.BorrowingViewSet)
router.register(r'libraries', views.LibraryViewSet)
router.register(r'borrowingswithborrower', views.BorrowingWithBorrowerViewSet)
router.register(r'booksPerLibrary', views.BooksPerLibraryViewSet)

urlpatterns = patterns('',
    # General urls
    url(r'^$', views.index, name='index'),
    url(r'^library/', views.library, name='library'),
    
    # Admin section
    url(r'^admin/', include(admin.site.urls)),
    
    # Api section
    url(r'^api/v1/borrowed-items', views.ListBorrowedItemsView.as_view()),
    url(r'^api/v1/items/borrowing-count', views.ItemBorrowingCountView.as_view()),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
