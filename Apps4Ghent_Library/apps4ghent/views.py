from django.shortcuts import render_to_response
from django.db import connection
from rest_framework import viewsets, views, generics
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django_filters import *
from .serializers import *
from .filters import *
from .utils import dictfetchall, get_paginated_response_from_queryset

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

class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @list_route()
    def borrowing_count(self, request):
        # List of item attributes that should be fetched
        item_attributes = ['id', 'title']

        values = list(map(lambda x: 'item_copy__item__' + x, item_attributes))
        queryset = Borrowing.objects.values(*values).annotate(count=Count('item_copy__item__id'))
        return get_paginated_response_from_queryset(self, queryset, ItemBorrowingCountSerializer)

class ItemCopyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItemCopy.objects.all()
    serializer_class = ItemCopySerializer

class SectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

class BorrowerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer

    @list_route()
    def count(self, request):
        queryset = self.get_queryset().values('sector').annotate(bcount=Count('pk'))
        return get_paginated_response_from_queryset(self, queryset, BorrowerCountSerializer)

class BorrowingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

class LibraryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class BorrowingWithBorrowerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingWithBorrowerSerializer

class ListBorrowedItemsView(generics.ListAPIView):
    queryset = Borrowing.objects.values('item_copy__location', 'borrower__sector_id').annotate(bcount=Count('pk'))
    serializer_class = BorrowedItemSerializer
    filter_class = BorrowedItemFilter

class BooksPerLibraryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItemCopy.objects.filter(copy_pk__icontains='HB')
    serializer_class = ItemCopySerializer
