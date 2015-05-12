from rest_framework import serializers
from .models import *

#serializer for an item
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item

#serializer for the amount of times a certain item has been borrowed
class ItemBorrowingCountSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='item_copy__item__id')
    title = serializers.CharField(source='item_copy__item__title')
    borrowing_count = serializers.IntegerField(source='count')

#serializer for a ItemCopy
class ItemCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCopy

#serializer for a sector
class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector

#serializer for a borrower
class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower

#serializer for the amount of borrowers for each sector
class BorrowerCountSerializer(serializers.Serializer):
    sector = serializers.IntegerField()
    borrower_count = serializers.IntegerField(source='bcount')

#serlializer for a borrowing
class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing

#serializer for borrowings together with the borrower and borrowed items
class BorrowingWithBorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        depth = 2

#serializer for libraries
class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library

#This serializer is used to serialize BorrowedItems from the views file
class BorrowedItemSerializer(serializers.Serializer):
    from_library = serializers.CharField(source='item_copy__location')
    to_sector = serializers.IntegerField(source='borrower__sector_id')
    borrowing_count = serializers.IntegerField(source='bcount')

#Here the amount of books of a borrower is serialized
class BorrowerCountSerializer(serializers.Serializer):
    borrower_count = serializers.IntegerField(source='bcount')
