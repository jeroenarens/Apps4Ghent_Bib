from django.db.models import *

class Library(Model):
    """Contains data about the different library branches"""
    # Primary key
    branch_code = CharField(max_length=5, primary_key=True)
    name = CharField(max_length=255)
    location = CharField(max_length=255)
    longitude = DecimalField(max_digits=17, decimal_places=14)
    latitude = DecimalField(max_digits=17, decimal_places=14)

    def __str__(self):
        return self.branch_code

    class Meta:
        db_table = 'libraries'

class Item(Model):
    """Represents an item present in the library (e.g. a book),
        storing mostly its description"""
    id = AutoField(primary_key=True)
    category_music = CharField(max_length=50,null=True)
    type = CharField(max_length=30,null=True)
    title = TextField(null=True)
    author_type = CharField(max_length=30,null=True)
    isbn_wrong = CharField(max_length=50,null=True)
    category_youth = CharField(max_length=50,null=True)
    issn = CharField(max_length=30,null=True)
    language = CharField(max_length=50,null=True)
    ean = CharField(max_length=30,null=True)
    age = CharField(max_length=30,null=True)
    series_edition = CharField(max_length=255,null=True)
    keywords_youth = CharField(max_length=128,null=True)
    author_lastname = CharField(max_length=128,null=True)
    publisher = CharField(max_length=255,null=True)
    author_firstname = CharField(max_length=128,null=True)
    keywords_libraries = CharField(max_length=128,null=True)
    year_published = CharField(max_length=128,null=True)
    keywords_local = CharField(max_length=128,null=True)
    pages = CharField(max_length=255,null=True)
    category_adults = CharField(max_length=64,null=True)
    siso = CharField(max_length=64,null=True)
    literarytype = CharField(max_length=64,null=True)
    ean_wrong = CharField(max_length=64,null=True)
    isbn = CharField(max_length=64,null=True)
    issn_wrong = CharField(max_length=64, null=True)
    siso_libraries = CharField(max_length=64, null=True)
    avi = CharField(max_length=16, null=True)
    openvlaccid = CharField(max_length=16, null=True)
    keyword_adults = CharField(max_length=128, null=True)
    zizo = CharField(max_length=16, null=True)
    series_title = CharField(max_length=255, null=True)
    keyword_youth = CharField(max_length=64, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'items'

class ItemCopy(Model):
    """Represent a physical copy of an item."""
    id = AutoField(primary_key=True)
    barcode = CharField(max_length=64, null=True)
    nature = IntegerField(null=True)
    #bb_number = IntegerField()
    item = ForeignKey(Item, db_column='item_id', related_name='item_copy_set', null=True)
    copy_pk = CharField(max_length=128, null=True)
    in_date = CharField(max_length=10, null=True)
    location = ForeignKey(Library, db_column='location', related_name='item_copy_set', null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'items_copy'
        
class Sector(Model):
    """Represents a sector of Ghent"""
    id = AutoField(primary_key=True)
    name = CharField(max_length=64,null=True)
    number = IntegerField(null=True)
    area = FloatField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sectors'

class Borrower(Model):
    """Represents a person who borrows something from the library."""
    id = AutoField(primary_key=True)
    lid_number = CharField(max_length=64,null=True)
    decade = IntegerField(null=True)
    sex = CharField(max_length=1,null=True)
    sector = CharField(max_length=64,null=True)
    postcode_start = CharField(max_length=1,null=True)
    subscription_year = IntegerField(null=True)
    subscription_location = CharField(max_length=8,null=True)
    category = CharField(max_length=8,null=True)
    sector_number = IntegerField(null=True)
    sector = ForeignKey(Sector, db_column='sector_id', related_name='borrower_set', null=True)

    def __str__(self):
        return self.lid_number

    class Meta:
        db_table = 'borrowers'

class Borrowing(Model):
    """Represents an instance of a borrowing of an item, containing information like dates and the profile of the person that borrowed the item."""
    id = AutoField(primary_key=True)
    from_date = DateField(null=True)
    lid_number = CharField(max_length=64,null=True)
    barcode = CharField(max_length=64, null=True)
    loan_period = IntegerField(null=True)
    item_copy = ForeignKey(ItemCopy, db_column='item_copy_id', related_name='borrowing_set_item', null=True)
    borrower = ForeignKey(Borrower, db_column='borrower_id', related_name='borrowing_set_borrower', null=True)
    
    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'borrowings'

