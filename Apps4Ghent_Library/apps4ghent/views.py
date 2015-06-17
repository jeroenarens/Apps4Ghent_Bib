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

#This view is used for the REC, to render the top 10 of summer books rented from the library of Ghent during the period of 2009-2014
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
            category = form.cleaned_data['category']
            borrowings = DenormalisedBorrowing.objects.filter(decade=decade, sex=sex, type='Boek', literarytype=category)

            #Now, get the books from the last 5 years during the summer months
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
            borrowings = borrowings.values('item_id', 'title', 'author_firstname','author_lastname', 'isbn').annotate(count=Count('item_id')).order_by('-count')[:52]
            #return the top 10

            context['items'] = borrowings
            return render_to_response('summerbooks.html', context)

    return render_to_response('index.html',{'form': form})


#can be ignored
def library(request):
    return render_to_response('library.html')


#From here on the views for the API are defined
#API view for the items
class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_class = ItemFilter

#API view for the items together with the total amount the item is borrowed
class ItemBorrowingCountView(generics.ListAPIView):
    queryset = DenormalisedBorrowing.objects.values('item_copy_id', 'title').annotate(count=Count('item_id'))
    serializer_class = ItemBorrowingCountSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filter_class = BorrowedItemFilter
    ordering_fields = ('count',)
    ordering = ('-count',)

#API view for the item_copies (exemplaar)
class ItemCopyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItemCopy.objects.all()
    serializer_class = ItemCopySerializer
    filter_class = ItemCopyFilter

#API view for the sectors in Ghent (wijken)
class SectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    filter_class = SectorFilter

#API view for the borrowers, together with a count function to get the amount of borrowers in each sector
class BorrowerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer
    filter_class = BorrowerFilter

    @list_route()
    def count(self, request):
        queryset = self.get_queryset().values('sector').annotate(bcount=Count('pk'))
        return get_paginated_response_from_queryset(self, queryset, BorrowerCountSerializer)

#API view for the borrowings
class BorrowingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DenormalisedBorrowing.objects.all()
    serializer_class = BorrowingSerializer
    filter_class = BorrowingFilter

#API view for the libraries
class LibraryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    filter_class = LibraryFilter



#Can be ignored
class BorrowingWithBorrowerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingWithBorrowerSerializer

#API view for the Borrowed items with respect to the location and the borrower and the count how much it is rent to each sector
class ListBorrowedItemsView(generics.ListAPIView):
    queryset = DenormalisedBorrowing.objects.values('location', 'sector').annotate(bcount=Count('pk'))
    serializer_class = BorrowedItemSerializer
    filter_class = BorrowedItemFilter

#API view for the items
class BooksPerLibraryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItemCopy.objects.filter(copy_pk__icontains='HB')
    serializer_class = ItemCopySerializer
