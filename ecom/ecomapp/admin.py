from django.contrib import admin
from .models import Product,Cart,Order,Address

# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display=['pid','pname','category','desc',"price",'image']

class cartAdmin(admin.ModelAdmin):
    list_display=['pid','quantity','date_added']

class orderAdmin(admin.ModelAdmin):
    list_display=['pid','quantity','date_added','user','is_completed']

class addressAdmin(admin.ModelAdmin):
    list_display=['user','address','zip','phone']


admin.site.register(Product,productAdmin)
admin.site.register(Cart,cartAdmin)
admin.site.register(Order,orderAdmin)
admin.site.register(Address,addressAdmin)