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

class ItemMethodsTest(TestCase):
    def setUp(self):
        item = Item.objects.create(BB_number="SOMEBBNUMBER1", title="Some title")
        item_copy = ItemCopy.objects.create(barcode="SOMEBARCODE1", item=item)
        borrower1 = Borrower.objects.create(borrower_id=1, borrower="Some guy", sector="SECTOR1", postcode=9000)
        borrower2 = Borrower.objects.create(borrower_id=2, borrower="Some guy 2", sector="SECTOR2", postcode=9001)
        borrowing1 = Borrowing.objects.create(bid=1, from_date=datetime.date(2015, 1, 1), loan_period=32, item_copy=item_copy, borrower=borrower1)
        borrowing2 = Borrowing.objects.create(bid=2, from_date=datetime.date(2015, 2, 18), loan_period=10, item_copy=item_copy, borrower=borrower2)
        
        item.item_copies.append(item_copy)
        item.save()
        item_copy.borrowings.append(borrowing1)
        item_copy.borrowings.append(borrowing2)
        item_copy.save()

    def test_get_borrowings_returns_correct_list_for_dates(self):
        item = Item.objects.get(pk="SOMEBBNUMBER1")
        borrowing1 = Borrowing.objects.get(pk=1)
        borrowing2 = Borrowing.objects.get(pk=2)

        borrowings = item.get_borrowings()
        has_borrowings = item.has_borrowings()
        self.assertTrue(has_borrowings)
        self.assertEqual(len(borrowings), 2)

        borrowings = item.get_borrowings(from_date=datetime.date(2015, 2, 19))
        has_borrowings = item.has_borrowings(from_date=datetime.date(2015, 2, 19))
        self.assertFalse(has_borrowings)
        self.assertEqual(len(borrowings), 0)

        borrowings = item.get_borrowings(from_date=datetime.date(2015, 1, 16))
        has_borrowings = item.has_borrowings(from_date=datetime.date(2015, 1, 16))
        self.assertTrue(has_borrowings)
        self.assertEqual(len(borrowings), 1)
        self.assertEqual(borrowings[0], borrowing2)

        borrowings = item.get_borrowings(from_date=datetime.date(2014, 9, 3))
        has_borrowings = item.has_borrowings(from_date=datetime.date(2014, 9, 3))
        self.assertTrue(has_borrowings)
        self.assertEqual(len(borrowings), 2)

        borrowings = item.get_borrowings(until_date=datetime.date(2014, 10, 13))
        has_borrowings = item.has_borrowings(until_date=datetime.date(2014, 10, 13))
        self.assertFalse(has_borrowings)
        self.assertEqual(len(borrowings), 0)

        borrowings = item.get_borrowings(until_date=datetime.date(2015, 2, 5))
        has_borrowings = item.has_borrowings(until_date=datetime.date(2015, 2, 5))
        self.assertTrue(has_borrowings)
        self.assertEqual(borrowings[0], borrowing1)

        borrowings = item.get_borrowings(until_date=datetime.date(2015, 3, 20))
        has_borrowings = item.has_borrowings(until_date=datetime.date(2015, 3, 20))
        self.assertTrue(has_borrowings)
        self.assertEqual(len(borrowings), 2)
