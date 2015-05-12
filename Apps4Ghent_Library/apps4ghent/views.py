from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db import connection
from rest_framework import viewsets, views, generics
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.filters import OrderingFilter, DjangoFilterBackend
from django_filters import *
from .serializers import *
from .filters import *
from .utils import dictfetchall, get_paginated_response_from_queryset, prefix_list
from datetime import *
from .forms import *

def index(request):
    context = RequestContext(request)
    form = booksform()
    if request.method == 'POST':
        form = booksform(request.POST)
        if form.is_valid():
            context = dict()
            #Get all the borrowings of persons of a certain category
            decade = form.cleaned_data['decade']
            sex = form.cleaned_data['sex']
            borrower = Borrower.objects.filter(decade=decade, sex=sex)
            borrowings = Borrowing.objects.filter(borrower=borrower,item_copy__item__type='Boek')

            #Now, get the books from the last 5 years:
            summer_start = date(2009,6,21)
            summer_end = date(2014,9,21)
            summermonths=[6,7,8,9]
            borrowings = borrowings.filter(Q(from_date__month=6)|
                                           Q(from_date__month=7)|
                                           Q(from_date__month=8)|
                                           Q(from_date__month=9))
            borrowings = borrowings.filter(Q(from_date__year=2009)|
                                           Q(from_date__year=2010)|
                                           Q(from_date__year=2011)|
                                           Q(from_date__year=2012)|
                                           Q(from_date__year=2013)|
                                           Q(from_date__year=2014))
            #get the item_copies of the most rent items
            #borrowings = borrowings.annotate(bcount=Count('barcode')).order_by('-bcount')[:10]
            borrowings = borrowings.values(*prefix_list('item_copy__item__', ['id', 'title', 'author_firstname','author_lastname', 'isbn'])).annotate(count=Count('item_copy__item__id')).order_by('-count')[2:12]
            #itemcopies = ItemCopy.objects.annotate(bcount=Count('borrowing_set_item')).order_by('-bcount')[:10]
            #return the top 10
            context['items'] = borrowings
            #context['itemcopies'] = itemcopies
            return render_to_response('overview.html', context)

    return render_to_response('index2.html',{'form': form})

def overview(request, form):
    context = dict()

    #Get all the borrowings of persons of a certain category
    borrower = Borrower.objects.filter(decade=1970, sex='M')
    borrowings = Borrowing.objects.filter(borrower=borrower,item_copy__item__type='Boek')

    #Now, get the books from the last 5 years:
    summer_start = date(2009,6,21)
    summer_end = date(2014,9,21)
    borrowings = borrowings.filter(from_date__gte=summer_start, from_date__lte=summer_end)

    #get the item_copies of the most rent items
    #borrowings = borrowings.annotate(bcount=Count('barcode')).order_by('-bcount')[:10]
    borrowings = borrowings.values(*prefix_list('item_copy__item__', ['id', 'title', 'author_firstname','author_lastname', 'isbn'])).annotate(count=Count('item_copy__item__id')).order_by('-count')[:10]
    #itemcopies = ItemCopy.objects.annotate(bcount=Count('borrowing_set_item')).order_by('-bcount')[:10]
    #return the top 10
    context['items'] = borrowings
    #context['itemcopies'] = itemcopies
    return render_to_response('overview.html', context)

def leaflet(request):
    return render_to_response('leaflet.html')

def openlayers(request):
    return render_to_response('openlayers.html')

def highmap(request):
    return render_to_response('highmaps.html')

class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_class = ItemFilter

class ItemBorrowingCountView(generics.ListAPIView):
    queryset = Borrowing.objects.values(*prefix_list('item_copy__item__', ['id', 'title'])).annotate(count=Count('item_copy__item__id'))
    serializer_class = ItemBorrowingCountSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filter_class = BorrowedItemFilter
    ordering_fields = ('count',)
    ordering = ('-count',)

class ItemCopyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItemCopy.objects.all()
    serializer_class = ItemCopySerializer

class SectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

class BorrowerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer

    @list_route()
    def count(self, request):
        queryset = self.get_queryset().values('sector').annotate(bcount=Count('pk'))
        return get_paginated_response_from_queryset(self, queryset, BorrowerCountSerializer)

class BorrowingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

class LibraryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class BorrowingWithBorrowerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingWithBorrowerSerializer

class ListBorrowedItemsView(generics.ListAPIView):
    queryset = Borrowing.objects.values('item_copy__location', 'borrower__sector_id').annotate(bcount=Count('pk'))
    serializer_class = BorrowedItemSerializer
    filter_class = BorrowedItemFilter

class BooksPerLibraryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItemCopy.objects.filter(copy_pk__icontains='HB')
    serializer_class = ItemCopySerializer
