from .models import *
from rest_framework_mongoengine.serializers import DocumentSerializer

class ItemSerializer(DocumentSerializer):
    class Meta:
        model = Item

class ItemCopySerializer(DocumentSerializer):
    class Meta:
        model = ItemCopy
