from django.shortcuts import render_to_response
from django.db import connection
from rest_framework import viewsets, views, generics
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.filters import OrderingFilter, DjangoFilterBackend
from django_filters import *
from .serializers import *
from .filters import *
from .utils import dictfetchall, get_paginated_response_from_queryset, prefix_list

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

class ItemBorrowingCountView(generics.ListAPIView):
    queryset = Borrowing.objects.values(*prefix_list('item_copy__item__', ['id', 'title'])).annotate(count=Count('item_copy__item__id'))
    serializer_class = ItemBorrowingCountSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filter_class = BorrowedItemFilter
    ordering_fields = ('count',)
    ordering = ('-count',)

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
