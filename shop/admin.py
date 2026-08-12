from django.contrib import admin
from .models import Category,Product,Cart,CartItem,Order,OrderItem,Favorite

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=("name","slug")
    prepopulated_fields={"slug":("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=("name","category","price","stock","rating","is_active")
    list_filter=("category","is_active")
    search_fields=("name","description")
    prepopulated_fields={"slug":("name",)}

class OrderItemInline(admin.TabularInline):
    model=OrderItem
    extra=0
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=("id","user","full_name","phone","status","total","created_at")
    list_filter=("status",)
    inlines=[OrderItemInline]
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
