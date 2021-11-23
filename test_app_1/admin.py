from django.contrib import admin
from .models import SKU, Warehouse, Purchase_Order, Plain_Carton_Line_Item

# Register your models here.


class SKUAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General information', {'fields': ['id','sku','required_pcs_fba_send_in_GERMANY', 'required_pcs_fba_send_in_FRANCE']}),
    ]
    list_display = ('id','sku','required_pcs_fba_send_in_GERMANY', 'required_pcs_fba_send_in_FRANCE')

class WarehouseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General information', {'fields': ['id','warehouse_name']}),
    ]
    list_display = ('id','warehouse_name')

class Purchase_OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General information', {'fields': ['id','order_name','warehouse', 'status']}),
    ]
    list_display = ('id','order_name','warehouse', 'status')

class Plain_Carton_Line_ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General information', {'fields': ['id','purchase_order','qty_cartons', 'cartons_left_cached', 'sku_obj', 'pcs_per_carton']}),
    ]
    list_display = ('id','purchase_order','qty_cartons', 'cartons_left_cached', 'sku_obj', 'pcs_per_carton')
    
admin.site.register(SKU, SKUAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Purchase_Order, Purchase_OrderAdmin)
admin.site.register(Plain_Carton_Line_Item, Plain_Carton_Line_ItemAdmin)
