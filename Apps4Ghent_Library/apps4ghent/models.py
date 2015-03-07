from mongoengine import *

# TODO: put blank constraints on the fields of models as soon as we get some example data 
class Item(Document):
    """Represents an item present in the library (e.g. a book),
    storing mostly its description"""
    
    # General information (can be used "outside library context")
    BB_number = StringField(max_length=45)
    title = StringField(max_length=45)
    ISBN = StringField(max_length=45)
    ISSN = StringField(max_length=45)
    material = StringField(max_length=45)
    visible_in_webopace = BooleanField()
    author_and_functions = StringField(max_length=45)

    # Information that can only be used "inside library context"
    number_of_pages = IntField()
    keywords = StringField(max_length=45)
    genre = StringField(max_length=45)
    theme = StringField(max_length=45)
    language = StringField(max_length=45)
    translated = StringField(max_length=1)
    literary_nature = StringField(max_length=45)
    edition = StringField(max_length=45)
    impressum = StringField(max_length=45)
    SISO = StringField(max_length=45)
    ZIZO = StringField(max_length=45)
    age_description = StringField(max_length=45)
    AVI = StringField(max_length=45)
    complete_title = StringField(max_length=45)

class ItemCopy(Document):
    """Represent a physical copy of an item."""

    barcode = StringField(max_length=45)
    location = StringField(max_length=45)
    in_date = DateTimeField()
    out_date = DateTimeField()
    last_intake_date = DateTimeField()
    last_borrowing_date = DateTimeField()
    kind = StringField(max_length=45)
    item = ReferenceField(Item)

class PersonProfile(EmbeddedDocument):
    """Represents the profile a person, as embedded inside borrowings and reservations."""
    sex = StringField(max_length=1)
    age = StringField(max_length=45)
    category = StringField(max_length=45)
    postcode = IntField()
    person_count = IntField()

class Borrowing(Document):
    """Represents an instance of a borrowing of an item, containing information like dates and the profile of the person that borrwed the item."""

    from_date = DateTimeField()
    until_date = DateTimeField()
    is_extended = BooleanField()

    item_copy = ReferenceField(ItemCopy)
    item = ReferenceField(Item)

    person_profile = EmbeddedDocumentField(PersonProfile)

class Reservation(Document):
    """Represents an instance of a reservation, containg information like dates and the profile of the person that reserved the item."""
    pickup_location = StringField(max_length=45)
    dropoff_location = StringField(max_length=45)
    request_date = DateTimeField()
    delivery_date = DateTimeField()
    pickup_date = DateTimeField()
    
    item_copy = ReferenceField(ItemCopy)
    item = ReferenceField(Item)

    person_profile = EmbeddedDocumentField(PersonProfile)
