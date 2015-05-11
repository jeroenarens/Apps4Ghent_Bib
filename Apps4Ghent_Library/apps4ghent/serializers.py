from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item

class ItemBorrowingCountSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='item_copy__item__id')
    title = serializers.CharField(source='item_copy__item__title')
    borrowing_count = serializers.IntegerField(source='count')

class ItemCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCopy

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower

class BorrowerCountSerializer(serializers.Serializer):
    sector = serializers.IntegerField()
    borrower_count = serializers.IntegerField(source='bcount')

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
    from_library = serializers.CharField(source='item_copy__location')
    to_sector = serializers.IntegerField(source='borrower__sector_id')
    borrowing_count = serializers.IntegerField(source='bcount')
