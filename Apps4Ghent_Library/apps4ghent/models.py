from django.db.models import *
class Item(Model):
    """Represents an item present in the library (e.g. a book),
        storing mostly its description"""
    id = AutoField(primary_key=True)
    bbnr = IntegerField()
    category_music = TextField()
    type = TextField()
    title = TextField()
    author_type = TextField()
    isbn_wrong = TextField()
    category_youth = TextField()
    issn = TextField()
    language = TextField()
    ean = TextField()
    age = TextField()
    series_edition = TextField()
    keywords_youth = TextField()
    author_lastname = TextField()
    publisher = TextField()
    author_firstname = TextField()
    keywords_libraries = TextField()
    year_published = TextField()
    keywords_local = TextField()
    pages = TextField()
    category_adults = TextField()
    siso = TextField()
    literarytype = TextField()
    ean_wrong = TextField()
    isbn = TextField()
    issn_wrong = TextField()
    siso_libraries = TextField()
    avi = TextField()
    openvlaccid = TextField()
    keyword_adults = TextField()
    zizo = TextField()
    series_title = TextField()
    keyword_youth = TextField()
    na = TextField()

    class Meta:
        db_table = 'items'

class ItemCopy(Model):
    """Represent a physical copy of an item."""
    id = AutoField(primary_key=True)
    copy_id = TextField()
    barcode = TextField()
    nature = IntegerField()
    bb_number = IntegerField()
    copy_pk = TextField()
    in_date = TextField()

    class Meta:
        db_table = 'items_copy'
        
class Sector(Model):
    """Represents a sector of Ghent"""
    id = AutoField(primary_key=True)
    name = TextField()
    number = IntegerField()
    cartodb_id = IntegerField()

    class Meta:
        db_table = 'sectors'

class Borrower(Model):
    """Represents a person who borrows something from the library."""
    id = AutoField(primary_key=True)
    lid_number = TextField()
    decade = IntegerField()
    sex = CharField(max_length=1)
    sector = TextField()
    postcode_start = TextField()
    subscription_year = IntegerField()
    subscription_location = TextField()
    category = TextField()
    sector_number = IntegerField()

    class Meta:
        db_table = 'borrowers'

class Borrowing(Model):
    """Represents an instance of a borrowing of an item, containing information like dates and the profile of the person that borrowed the item."""
    id = AutoField(primary_key=True)
    borrowing_id = IntegerField()
    from_date = TextField()
    lid_number = TextField()
    barcode = TextField()
    loan_period = IntegerField()

    class Meta:
        db_table = 'borrowings'
