from mongoengine import Document, StringField, IntField, BooleanField

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
