from django.contrib import admin
from import_export.admin import ExportMixin, ExportActionMixin

from .models import StockItem, StockIssuanceLogEntry, StockReplenishmentLogEntry

# Register your models here.

class StockItemAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "item_name", "identification_num", "item_type", 
        "mfr_part_num", "min_level", "max_level", "stock_balance",
        "needs_to_be_replenished", "remarks"
    )

admin.site.register(StockItem, StockItemAdmin)

class StockIssuanceLogEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id", "stock_item", "date_of_issuance", "quantity_issued", "issued_to", "issued_by", "remarks"
    )

admin.site.register(StockIssuanceLogEntry, StockIssuanceLogEntryAdmin)

class StockReplenishmentLogEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id", "stock_item", "date_of_replenishment", "quantity_added", "updated_by", "remarks"
    )

admin.site.register(StockReplenishmentLogEntry, StockReplenishmentLogEntryAdmin)
