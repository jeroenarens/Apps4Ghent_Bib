from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item

class ItemCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCopy

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower

class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing

class BorrowingWithBorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        depth = 2

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library

class BorrowedItemSerializer(serializers.Serializer):
    from_library = serializers.IntegerField()
    to_sector = serializers.IntegerField()
    borrowing_count = serializers.IntegerField()
