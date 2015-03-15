import datetime

from django.test import TestCase
from django.utils import timezone

from apps4ghent.models import *

class BorrowingMethodsTest(TestCase):

    def test_until_date_returns_correct_date(self):
        from_date = timezone.now()
        until_date = from_date + datetime.timedelta(days=10)
        borrowing = Borrowing.objects.create(bid=1, from_date=from_date, loan_period=10)
        self.assertEqual(borrowing.until_date(), until_date)
