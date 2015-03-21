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

   return render_to_response('index2.html')

def overview(request):
    return render_to_response('overview.html')

def leaflet(request):
    return render_to_response('leaflet.html')

def highmap(request):
    return render_to_response('highmaps.html')

class Paginator:
    page_size = 100
    max_page_size=1000
    page_query_param='page'
    page_size_query_param='page_size'

    def paginate_queryset(self, queryset, page=0, page_size=100):
        count = len(queryset) #queryset.count()
        start_index = page * page_size
        end_index = min(start_index + page_size, count)
        return queryset[start_index:end_index] if (start_index < end_index) else []

    def paginate(self, request, queryset):
        page = int(request.QUERY_PARAMS.get('page', 0))
        page_size = int(request.QUERY_PARAMS.get('page_size', getattr(self, 'page_size')))
        queryset = self.paginate_queryset(queryset, page, page_size)
        return queryset

class ReadOnlyDocumentViewSet(ViewSet):
    """Viewset for mongodb documents that provides an implementation for `list` and `retrieve`"""
    pagination_class = Paginator

    def list(self, request):
        model_cls = getattr(self, 'model', None)
        serializer_cls = getattr(self, 'serializer_class', None)
        assert model_cls, '`model` argument not specified, cannot proceed.'
        assert serializer_cls, '`serializer_class` argument not specified, cannot proceed.'
        paginator = getattr(self, 'pagination_class')()
        queryset = paginator.paginate(request, model_cls.objects.all())
        serializer = serializer_cls(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        model_cls = getattr(self, 'model', None)
        serializer_cls = getattr(self, 'serializer_class', None)
        assert model_cls, '`model` argument not specified, cannot proceed.'
        assert serializer_cls, '`serializer_class` argument not specified, cannot proceed'

        paginator = getattr(self, 'pagination_class')()
        queryset = paginator.paginate(request, model_cls.objects.all())
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
    pagination_class = Paginator

    def get_items_queryset(self):
        # Perform basic filtering
        filtered_qs = super(BorrowedItemsView, self).get_queryset()

        # Get dates to filter on
        from_date = dateparse.parse_date(self.request.QUERY_PARAMS.get('from_date', ''))
        until_date = dateparse.parse_date(self.request.QUERY_PARAMS.get('until_date', ''))
        
        # Get locations to filter on
        sector = self.request.QUERY_PARAMS.get('sector', '')

        # Do actual filtering
        filtered_items = []
        for item in filtered_qs:
            # Save the fetched borrowings as a property of an item
            item.cached_borrowings = item.get_borrowings(from_date=from_date, until_date=until_date, to_sector=sector)
            if item.cached_borrowings:
                filtered_items.append(item)

        return filtered_items

    def get_queryset(self):
        # Get items
        filtered_items = self.get_items_queryset()

        # Do pagination
        paginator = getattr(self, 'pagination_class')()
        return paginator.paginate(self.request, filtered_items)

class BorrowedItemsBorrowingsView(BorrowedItemsView):
    serializer_class = BorrowedItemsBorrowingsSerializer
    def get_borrowings_queryset(self):
        filtered_items = super(BorrowedItemsBorrowingsView, self).get_items_queryset()
        filtered_borrowings = map(lambda item: item.cached_borrowings, filtered_items)
        flattened_borrowings = [el for sublist in filtered_borrowings for el in sublist]

        return flattened_borrowings

    def get_queryset(self):
        # Get borrowings
        flattened_borrowings = self.get_borrowings_queryset()

        # Do pagination
        paginator = getattr(self, 'pagination_class')()
        return paginator.paginate(self.request, flattened_borrowings)
    
class BorrowedItemsBorrowingsCountView(BorrowedItemsBorrowingsView):
    def get(self, request, format=None):
        # TODO This can be done in a more performant efficient manner
        borrowings = self.get_borrowings_queryset()
        return Response(len(borrowings))
