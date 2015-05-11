import django_filters

from .models import *

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

