from django.shortcuts import  render, render_to_response
from rest_framework_mongoengine.generics import ListAPIView
from .serializers import *

def index(request):
   return render_to_response('index.html')

class ItemList(ListAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class ItemCopyList(ListAPIView):
    serializer_class = ItemCopySerializer
    queryset = ItemCopy.objects.all()

class BorrowerList(ListAPIView):
    serializer_class = BorrowerSerializer
    queryset = Borrower.objects.all()

class BorrowingList(ListAPIView):
    serializer_class = BorrowingSerializer
    queryset = Borrowing.objects.all()

class ReservationList(ListAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

