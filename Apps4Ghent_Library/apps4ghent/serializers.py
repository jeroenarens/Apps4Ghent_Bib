from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item

class ItemCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCopy

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
