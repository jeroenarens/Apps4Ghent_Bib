from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item

class ItemCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCopy
