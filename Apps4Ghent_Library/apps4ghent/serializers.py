from .models import *
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers

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

class EmbeddedBorrowingSerializer(DocumentSerializer):
    from_library = serializers.CharField(read_only=True)
    to_sector = serializers.CharField(read_only=True)
    borrowing_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Borrowing
        fields = ('from_library', 'to_sector', 'borrowing_count')

class ReservationSerializer(DocumentSerializer):
    class Meta:
        model = Reservation

class BorrowedItemSerializer(DocumentSerializer):
    borrowings = EmbeddedBorrowingSerializer(source='get_borrowings', read_only=True, many=True)
    class Meta:
        model = Item
        depth = 2
        fields = ('BB_number', 'title', 'ISBN', 'item_type', 'borrowings')

