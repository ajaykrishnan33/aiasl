from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StockItem(models.Model):
    ITEM_TYPE_OPTIONS = (
        ("oils", "Oils"),
        ("filters", "Filters"),
        ("commercial_items", "Commercial Items"),
        ("equipment_spares", "Equipment Spares"),
        ("misc", "Miscellaneous")
    )
    UOM_OPTIONS = (
        ("number", "Number"),
        ("litre", "Litres"),
        ("kg", "Kg")
    )
    item_type = models.CharField(max_length=50, choices=ITEM_TYPE_OPTIONS)
    item_name = models.CharField(max_length=256)
    identification_num = models.CharField(max_length=20)
    mfr_part_num = models.CharField(max_length=20, null=True, blank=True)
    min_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_of_measure = models.CharField(max_length=10, choices=UOM_OPTIONS)
    stock_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    needs_to_be_replenished = models.BooleanField(default=False, editable=False)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} ({})".format(self.item_name, self.identification_num)
    
    def check_if_needs_to_be_replenished(self):
        if self.stock_balance < self.min_level:
            self.needs_to_be_replenished = True
        else:
            self.needs_to_be_replenished = False
    
    def add(self, quantity):
        self.stock_balance += quantity
    
    def remove(self, quantity):
        self.stock_balance -= quantity
    
    def save(self, *args, **kwargs):
        self.check_if_needs_to_be_replenished()
        super().save(*args, **kwargs)

class StockIssuanceLogEntry(models.Model):
    stock_item = models.ForeignKey(StockItem, related_name="issuance_log_entries", on_delete=models.DO_NOTHING)
    date_of_issuance = models.DateTimeField(auto_now_add=True)
    quantity_issued = models.DecimalField(max_digits=10, decimal_places=2)
    issued_to = models.ForeignKey(User, related_name="issued_to_logs", on_delete=models.DO_NOTHING)
    issued_by = models.ForeignKey(User, related_name="issued_by_logs", on_delete=models.DO_NOTHING)
    remarks = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.stock_item.remove(self.quantity_issued)
        self.stock_item.check_if_needs_to_be_replenished()
        self.stock_item.save()

class StockReplenishmentLogEntry(models.Model):
    stock_item = models.ForeignKey(StockItem, related_name="replenishment_log_entries", on_delete=models.DO_NOTHING)
    date_of_replenishment = models.DateTimeField(auto_now_add=True)
    quantity_added = models.DecimalField(max_digits=10, decimal_places=2)
    updated_by = models.ForeignKey(User, related_name="replenished_by_logs", on_delete=models.DO_NOTHING)
    remarks = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.stock_item.add(self.quantity_added)
        self.stock_item.check_if_needs_to_be_replenished()
        self.stock_item.save()
