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

# TODO Items are filtered correctly on their before_date and until_date, but still all borrowings (even those outside the date range) are returned
class BorrowedItemsView(FilteredListAPIView):
    filter_class = ItemFilter
    queryset = Item.objects.all()
    serializer_class = BorrowedItemSerializer

    def get_queryset(self):
        # Perform basic filtering
        filtered_qs = super(BorrowedItemsView, self).get_queryset()

        from_date = dateparse.parse_date(self.request.QUERY_PARAMS.get('from_date', None) or '')
        until_date = dateparse.parse_date(self.request.QUERY_PARAMS.get('until_date', None) or '')
        filtered_qs = filter(lambda item: item.has_borrowings(from_date=from_date, until_date=until_date), filtered_qs)

        return filtered_qs
