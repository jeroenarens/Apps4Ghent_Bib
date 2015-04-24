from django.db.models import *
class Item(Model):
    """Represents an item present in the library (e.g. a book),
        storing mostly its description"""
    id = AutoField(primary_key=True)
    bbnr = IntegerField()
    category_music = CharField(max_length=50)
    type = CharField(max_length=30)
    title = TextField()
    author_type = CharField(max_length=30)
    isbn_wrong = CharField(max_length=50)
    category_youth = CharField(max_length=50)
    issn = CharField(max_length=30)
    language = CharField(max_length=50)
    ean = CharField(max_length=30)
    age = CharField(max_length=30)
    series_edition = CharField(max_length=255)
    keywords_youth = CharField(max_length=128)
    author_lastname = CharField(max_length=128)
    publisher = CharField(max_length=255)
    author_firstname = CharField(max_length=128)
    keywords_libraries = CharField(max_length=128)
    year_published = CharField(max_length=128)
    keywords_local = CharField(max_length=128)
    pages = CharField(max_length=255)
    category_adults = CharField(max_length=64)
    siso = CharField(max_length=64)
    literarytype = CharField(max_length=64)
    ean_wrong = CharField(max_length=64)
    isbn = CharField(max_length=64)
    issn_wrong = CharField(max_length=64)
    siso_libraries = CharField(max_length=64)
    avi = CharField(max_length=16)
    openvlaccid = CharField(max_length=16)
    keyword_adults = CharField(max_length=128)
    zizo = CharField(max_length=16)
    series_title = CharField(max_length=255)
    keyword_youth = CharField(max_length=64)
    na = TextField()

    class Meta:
        db_table = 'items'

class ItemCopy(Model):
    """Represent a physical copy of an item."""
    id = AutoField(primary_key=True)
    copy_id = CharField(max_length=32)
    barcode = CharField(max_length=64)
    nature = IntegerField()
    #bb_number = IntegerField()
    item = ForeignKey(Item, db_column='item_id')
    copy_pk = CharField(max_length=128)
    in_date = CharField(max_length=10)

    class Meta:
        db_table = 'items_copy'
        
class Sector(Model):
    """Represents a sector of Ghent"""
    id = AutoField(primary_key=True)
    name = CharField(max_length=64)
    number = IntegerField()
    cartodb_id = IntegerField()

    class Meta:
        db_table = 'sectors'

class Borrower(Model):
    """Represents a person who borrows something from the library."""
    id = AutoField(primary_key=True)
    lid_number = CharField(max_length=64)
    decade = IntegerField()
    sex = CharField(max_length=1)
    #sector = CharField(max_length=64)
    sector = ForeignKey(Sector, db_column='sector_id')
    postcode_start = CharField(max_length=1)
    subscription_year = IntegerField()
    subscription_location = CharField(max_length=8)
    category = CharField(max_length=8)
    #sector_number = IntegerField()

    class Meta:
        db_table = 'borrowers'

class Borrowing(Model):
    """Represents an instance of a borrowing of an item, containing information like dates and the profile of the person that borrowed the item."""
    id = AutoField(primary_key=True)
    borrowing_id = IntegerField()
    from_date = CharField(max_length=10)
    #lid_number = CharField(max_length=64)
    borrower = ForeignKey(Borrower, db_column='borrower_id')
    #barcode = CharField(max_length=64)
    item_copy = ForeignKey(ItemCopy, db_column='item_copy_id')
    loan_period = IntegerField()

    class Meta:
        db_table = 'borrowings'
