from rest_framework_mongoengine.generics import ListCreateAPIView
from .serializers import *

class ItemList(ListCreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
