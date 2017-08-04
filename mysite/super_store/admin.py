from django.contrib import admin
from .models import Product, Images, Skus, Brand


class ProductInLine(admin.TabularInline):
    model = Product
    extra = 0


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    fields = ('name', 'brand_link', 'image_icon', 'image_tag',)
    readonly_fields = ('image_tag',)
    inlines = [
        ProductInLine
    ]


class ImageInLine(admin.TabularInline):
    model = Images
    extra = 0


class SkusInLine(admin.TabularInline):
    model = Skus
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name',
                    'category', 'entry_date', 'update_date', 'brand')
    search_fields = ('product_id', 'product_name', 'category')
    list_filter = ('entry_date', 'update_date', 'brand')
    ordering = ('-entry_date',)
    fields = ('brand', 'product_id', 'product_name', 'category', 'source_url')

    inlines = [
        ImageInLine,
        SkusInLine
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Images)
admin.site.register(Skus)
admin.site.register(Brand, BrandAdmin)
