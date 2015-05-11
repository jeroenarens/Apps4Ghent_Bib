from django.shortcuts import render_to_response
from django.db import connection
from rest_framework import viewsets, views
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

class BorrowingWithBorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingWithBorrowerSerializer

class ListBorrowedItemsView(views.APIView):

    def fetch_data_from_db(self):
        # Perform raw SQL query for efficiency
        cursor = connection.cursor()
        cursor.execute("SELECT bb.sector_id AS to_sector, NULL AS from_library, COUNT(bb.sector_id) AS borrowing_count FROM items i INNER JOIN items_copy ic ON i.id = ic.item_id INNER JOIN borrowings b  ON b.item_copy_id = ic.id INNER JOIN borrowers  bb ON b.borrower_id = bb.id GROUP BY bb.sector_id;")

        # Fetch as dictionary
        return dictfetchall(cursor)

    def get(self, request, format=None):
        "Returns list of borrowed items"
        data = self.fetch_data_from_db()
        serializer = BorrowedItemSerializer(data, many=True)
        return Response(serializer.data)

class BooksPerLibraryViewSet(viewsets.ModelViewSet):
    queryset = ItemCopy.objects.filter(copy_pk__icontains='HB')
    serializer_class = ItemCopySerializer