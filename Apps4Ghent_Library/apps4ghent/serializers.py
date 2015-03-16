from collections import Counter
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
        depth = 2

class BorrowerSerializer(DocumentSerializer):
    class Meta:
        model = Borrower
        depth = 2

class BorrowingSerializer(DocumentSerializer):
    class Meta:
        model = Borrowing
        depth = 2

class EmbeddedBorrowingSerializer(DocumentSerializer):
    class Meta:
        model = Borrowing
        fields = ('from_library', 'to_sector', 'borrowing_count', 'from_date', 'until_date')
        depth = 2

class ReservationSerializer(DocumentSerializer):
    class Meta:
        model = Reservation
        depth = 2

class BorrowedItemSerializer(DocumentSerializer):
    borrowings = EmbeddedBorrowingSerializer(source='get_borrowings', read_only=True, many=True)
    class Meta:
        model = Item
        depth = 2
        fields = ('BB_number', 'title', 'ISBN', 'item_type', 'borrowings')

class BorrowedItemsBorrowingListSerializer(serializers.ListSerializer):
    def __init__(self, *args, **kwargs):
        args_list = list(args)
        args_list[0] = self.process_borrowings(args[0])
        args = tuple(args_list)
        super(BorrowedItemsBorrowingListSerializer, self).__init__(*args, **kwargs)

    def process_borrowings(self, borrowings):
        tuples = list(map(lambda b: (b.from_library(), b.to_sector()), borrowings))
        cnt = Counter(tuples)
        borrowings = list(map(lambda i: self.count_to_simple_borrowing(*i), cnt.most_common())) 
        return borrowings

    def count_to_simple_borrowing(self, borrowing_tuple, count):
        b = Borrowing()
        b.from_library_cached = borrowing_tuple[0]
        b.to_sector_cached = borrowing_tuple[1]
        b.borrowing_count_cached = count
        return b

class BorrowedItemsBorrowingsSerializer(DocumentSerializer):
    class Meta:
        model = Borrowing
        depth = 2
        fields = ('from_library', 'to_sector', 'borrowing_count')
        list_serializer_class = BorrowedItemsBorrowingListSerializer
