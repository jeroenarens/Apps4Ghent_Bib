import django_filters_mongoengine as filters
import django_filters

from django.utils import dateparse
from django.shortcuts import  render, render_to_response
from mongoengine.django.shortcuts import get_document_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .serializers import *

def index(request):
   return render_to_response('index.html')

class ReadOnlyDocumentViewSet(ViewSet):
    """Viewset for mongodb documents that provides an implementation for `list` and `retrieve`"""
    def list(self, request):
        model_cls = getattr(self, 'model', None)
        serializer_cls = getattr(self, 'serializer_class', None)
        assert model_cls, '`model` argument not specified, cannot proceed.'
        assert serializer_cls, '`serializer_class` argument not specified, cannot proceed.'

        queryset = model_cls.objects.all()
        serializer = serializer_cls(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        model_cls = getattr(self, 'model', None)
        serializer_cls = getattr(self, 'serializer_class', None)
        assert model_cls, '`model` argument not specified, cannot proceed.'
        assert serializer_cls, '`serializer_class` argument not specified, cannot proceed'

        queryset = model_cls.objects.all()
        document = get_document_or_404(queryset, pk=pk)
        serializer = serializer_cls(document)
        return Response(serializer.data)

class ItemsViewSet(ReadOnlyDocumentViewSet):
    model = Item
    serializer_class = ItemSerializer

class ItemCopyViewSet(ReadOnlyDocumentViewSet):
    model = ItemCopy
    serializer_class = ItemCopySerializer

class BorrowerViewSet(ReadOnlyDocumentViewSet):
    model = Borrower
    serializer_class = BorrowerSerializer

class BorrowingViewSet(ReadOnlyDocumentViewSet):
    model = Borrowing
    serializer_class = BorrowingSerializer

class ReservationViewSet(ReadOnlyDocumentViewSet):
    model = Reservation
    serializer_class = ReservationSerializer

class FilteredListAPIView(ListAPIView):
    def get_queryset(self):
        filter_cls = getattr(self, 'filter_class', None)
        queryset = getattr(self, 'queryset', None)
        assert filter_cls, '`filter_class` argument not specified, cannot proceed.'
        assert queryset, '`queryset` argument not specified, cannot proceed.'

        return filter_cls(self.request.GET, queryset=queryset).qs

class ItemFilter(filters.FilterSet):
    title = filters.StringFilter(lookup_type='icontains')
    class Meta:
        model = Item
        fields = ['ISBN', 'title']

class BorrowedItemsView(FilteredListAPIView):
    filter_class = ItemFilter
    queryset = Item.objects.all()
    serializer_class = BorrowedItemSerializer

    def get_queryset(self):
        # Perform basic filtering
        filtered_qs = super(BorrowedItemsView, self).get_queryset()

        from_date = dateparse.parse_date(self.request.QUERY_PARAMS.get('from_date', ''))
        until_date = dateparse.parse_date(self.request.QUERY_PARAMS.get('until_date', ''))

        filtered_items = []
        for item in filtered_qs:
            # Save the fetched borrowings as a property of an item
            item.cached_borrowings = item.get_borrowings(from_date=from_date, until_date=until_date)
            if item.cached_borrowings:
                filtered_items.append(item)

        return filtered_items

class BorrowedItemsBorrowingsView(BorrowedItemsView):
    serializer_class = BorrowedItemsBorrowingsSerializer
    def get_queryset(self):
        filtered_items = super(BorrowedItemsBorrowingsView, self).get_queryset()
        filtered_borrowings = map(lambda item: item.cached_borrowings, filtered_items)
        flattened_borrowings = [el for sublist in filtered_borrowings for el in sublist]
        return flattened_borrowings
    
class BorrowedItemsBorrowingsCountView(BorrowedItemsBorrowingsView):
    def get(self, request, format=None):
        # TODO This can be done in a more performant efficient manner
        borrowings = self.get_queryset()
        return Response(len(borrowings))
