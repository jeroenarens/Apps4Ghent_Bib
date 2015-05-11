import django_filters

from .models import *

class BorrowedItemFilter(django_filters.FilterSet):
    from_library = django_filters.CharFilter(name='item_copy__location')
    to_sector = django_filters.NumberFilter(name='borrower__sector_id')
    type = django_filters.CharFilter(name='item_copy__item__type')
    decade = django_filters.NumberFilter(name='borrower__decade')
    sex = django_filters.CharFilter(name='borrower__sex')

    class Meta:
        model = Borrowing
        fields = ['from_library', 'to_sector', 'type', 'decade', 'sex']

