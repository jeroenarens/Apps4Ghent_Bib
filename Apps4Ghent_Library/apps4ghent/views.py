from django.shortcuts import  render, render_to_response
from mongoengine.django.shortcuts import get_document_or_404
from rest_framework.viewsets import ViewSet
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

