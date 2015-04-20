from django.db.models import *
class Item(Model):
    """Represents an item present in the library (e.g. a book),
        storing mostly its description"""
    id = AutoField(primary_key=True)
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
