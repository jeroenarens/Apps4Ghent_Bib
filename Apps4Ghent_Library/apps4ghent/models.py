import datetime

from mongoengine import *

# TODO: put blank constraints on the fields of models as soon as we get some example data 
class Item(Document):
    """Represents an item present in the library (e.g. a book),
    storing mostly its description"""

    # General information (can be used "outside library context")
    BB_number = StringField(max_length=45, primary_key=True)
    year_published = StringField(max_length=45)
    ISBN = StringField(max_length=45)
    title = StringField(max_length=45)
    item_type = StringField(max_length=45) # material, kind
    ISSN = StringField(max_length=45)

    # Information that can only be used "inside library context"
    series_title = StringField(max_length=45)
    literarytype = StringField(max_length=45)
    language = StringField(max_length=45)
    age = StringField(max_length=45)

    SISO = StringField(max_length=45)
    SISO_libraries = StringField(max_length=45)
    ZIZO = StringField(max_length=45)
    AVI = StringField(max_length=45)
    EAN = StringField(max_length=45)

    category_youth = StringField(max_length=45)
    category_music = StringField(max_length=45)
    category_adults = StringField(max_length=45)

    keywords_local = StringField(max_length=45)
    keywords_youth = StringField(max_length=45)
    keywords_libraries = StringField(max_length=45)
    keyword_youth = StringField(max_length=45)
    keyword_adults = StringField(max_length=45)

    author_type = StringField(max_length=45)
    author_lastname = StringField(max_length=45)
    author_firstname = StringField(max_length=45)
    publisher = StringField(max_length=45)
    pages = IntField()
    series_edition = StringField(max_length=45)

    # Reverse relations
    item_copies = ListField(ReferenceField("ItemCopy"))

    def get_borrowings(self, from_date=None, until_date=None):
        """Returns a list of borrowings of the physical copies of this item."""

        filtered_borrowings = []
        for item_copy in self.item_copies:
            borrowings = item_copy.borrowings
            
            # Filter borrowings
            borrowings = filter(lambda b: b.from_date.date() >= from_date, borrowings) if from_date else borrowings
            borrowings = filter(lambda b: b.until_date().date() <= until_date, borrowings) if until_date else borrowings
            
            # Add results
            filtered_borrowings.extend(borrowings)
        return filtered_borrowings

    def has_borrowings(self, from_date=None, until_date=None):
        return not not self.get_borrowings(from_date=from_date, until_date=until_date)

class ItemCopy(Document):
    """Represent a physical copy of an item."""

    barcode = StringField(max_length=45, primary_key=True)
    location = StringField(max_length=45)
    in_date = DateTimeField()
    out_date = DateTimeField()
    last_intake_date = DateTimeField()
    last_borrowing_date = DateTimeField()
    kind = StringField(max_length=45)
    item = ReferenceField(Item)

    # Reverse relation
    borrowings = ListField(ReferenceField("Borrowing"))

class Borrower(Document):
    """Represents a person who borrows something from the library."""
    borrower_id = IntField(primary_key=True)
    borrower = StringField(max_length=45)
    sex = StringField(max_length=45)
    sector = StringField(max_length=45)
    postcode = IntField()
    subscription_year = IntField()
    subscription_location = StringField(max_length=45)
    category = StringField(max_length=45)

class Borrowing(Document):
    """Represents an instance of a borrowing of an item, containing information like dates and the profile of the person that borrwed the item."""

    bid = IntField(primary_key=True)
    from_date = DateTimeField()
    loan_period = IntField() # in days
    borrower = ReferenceField(Borrower)
    item_copy = ReferenceField(ItemCopy) # Barcode

    def from_library(self):
        return None # TODO

    def to_sector(self):
        return self.borrower.sector

    def borrowing_count(self):
        return 1 # TODO

    def until_date(self):
        """Returns a `DateTime` that specifies how long this borrowing is valid"""
        return self.from_date + datetime.timedelta(days=self.loan_period)

class Reservation(Document):
    """Represents an instance of a reservation, containg information like dates and the profile of the person that reserved the item."""
    pickup_location = StringField(max_length=45)
    dropoff_location = StringField(max_length=45)
    request_date = DateTimeField()
    delivery_date = DateTimeField()
    pickup_date = DateTimeField()
    
    item_copy = ReferenceField(ItemCopy)
    item = ReferenceField(Item)

    borrower = ReferenceField(Borrower)
