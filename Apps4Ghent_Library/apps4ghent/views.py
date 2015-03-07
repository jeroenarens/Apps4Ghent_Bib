from rest_framework_mongoengine.generics import ListCreateAPIView
from .serializers import *

class ItemList(ListCreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class ItemCopyList(ListCreateAPIView):
    serializer_class = ItemCopySerializer
    queryset = ItemCopy.objects.all()

class BorrowingList(ListCreateAPIView):
    serializer_class = BorrowingSerializer
    queryset = Borrowing.objects.all()

class ReservationList(ListCreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
