from .models import *
from rest_framework_mongoengine.serializers import DocumentSerializer

class ItemSerializer(DocumentSerializer):
    class Meta:
        model = Item
        depth = 2

class ItemCopySerializer(DocumentSerializer):
    class Meta:
        model = ItemCopy

class BorrowerSerializer(DocumentSerializer):
    class Meta:
        model = Borrower

class BorrowingSerializer(DocumentSerializer):
    class Meta:
        model = Borrowing

class ReservationSerializer(DocumentSerializer):
    class Meta:
        model = Reservation
