import django_filters

from .models import *

#This is used so you can filter how many books are sent from each library to each sector, together with filter parameters for borrowers and borrowings
class BorrowedItemFilter(django_filters.FilterSet):
    from_library = django_filters.CharFilter(name='item_copy__location')
    to_sector = django_filters.NumberFilter(name='borrower__sector_id')
    type = django_filters.CharFilter(name='item_copy__item__type')
    decade = django_filters.NumberFilter(name='borrower__decade')
    sex = django_filters.CharFilter(name='borrower__sex')
    from_date = django_filters.DateFilter(name='from_date', lookup_type='gte')
    until_date = django_filters.DateFilter(name='from_date', lookup_type='lte')

    class Meta:
        model = Borrowing
        fields = ['from_library', 'to_sector', 'type', 'decade', 'sex', 'from_date', 'until_date']

#This filter is used to filter on a certain - or collection of items
class ItemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(name='title', lookup_type='icontains')
    series_edition = django_filters.CharFilter(name='series_edition', lookup_type='icontains')
    class Meta:
        model = Item
        fields = ['title','id','category_music','type','author_type','isbn','category_youth','issn','language','ean','age','series_edition','keywords_youth','author_lastname','author_firstname','publisher','keywords_libraries','keywords_local','pages','category_adults','siso','literarytype','siso_libraries','openvlaccid','keyword_adults','zizo','series_title','keywords_youth']

#This filter is used to filter on a certain - or collection of item copies
class ItemCopyFilter(django_filters.FilterSet):
    class Meta:
        model = ItemCopy

#This filter is used to filter on a certain - or collection of borrowings
class BorrowingFilter(django_filters.FilterSet):
    class Meta:
        model = Borrowing

#This filter is used to filter on a certain - or collection of borrowers
class BorrowerFilter(django_filters.FilterSet):
    class Meta:
        model = Borrower

#This filter is used to filter on a certain - or collection of sectors
class SectorFilter(django_filters.FilterSet):
    class Meta:
        model = Sector

#This filter is used to filter on a certain - or collection of libraries
class LibraryFilter(django_filters.FilterSet):
    class Meta:
        model = Library