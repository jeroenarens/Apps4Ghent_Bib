from django.shortcuts import render_to_response
from django.db import connection
from rest_framework import viewsets, views, generics
from rest_framework.response import Response
from django_filters import *
from .serializers import *
from .utils import dictfetchall

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

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemCopyViewSet(viewsets.ModelViewSet):
    queryset = ItemCopy.objects.all()
    serializer_class = ItemCopySerializer

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer

class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class BorrowingWithBorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingWithBorrowerSerializer

class ListBorrowedItemsView(generics.ListAPIView):
    queryset = Borrowing.objects.values('item_copy__location', 'borrower__sector_id').annotate(bcount=Count('pk'))
    serializer_class = BorrowedItemSerializer

class BooksPerLibraryViewSet(viewsets.ModelViewSet):
    queryset = ItemCopy.objects.filter(copy_pk__icontains='HB')
    serializer_class = ItemCopySerializer
