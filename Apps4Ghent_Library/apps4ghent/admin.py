from django.contrib import admin
from .models import *
# Register your models here.
#When going to the BASE_url/admin, you can see the classes that are coded in here
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author_firstname', 'author_lastname', 'publisher', 'isbn')

class ItemCopyModel(admin.ModelAdmin):
    list_display = ('id', 'copy_pk', 'barcode')

class SectorModel(admin.ModelAdmin):
    list_display = ('id', 'name', 'number', 'area')

class BorrowerModel(admin.ModelAdmin):
    list_display = ('id', 'lid_number', 'decade', 'sex', 'postcode_start')

class BorrowingModel(admin.ModelAdmin):
    list_display = ('id', 'item_copy', 'borrower')

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemCopy, ItemCopyModel)
admin.site.register(Borrower, BorrowerModel)
admin.site.register(Borrowing, BorrowingModel)
admin.site.register(Sector, SectorModel)
