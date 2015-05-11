import django_filters

from .models import *

class BorrowedItemFilter(django_filters.FilterSet):
    from_library = django_filters.CharFilter(name='item_copy__location')
    to_sector = django_filters.NumberFilter(name='borrower__sector_id')

    class Meta:
        model = Borrowing
        fields = ['from_library', 'to_sector']

