from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Categories, Product


class ProductInline(admin.TabularInline):
    model = Product
    readonly_fields = ('preview',)
    fields = ('name', 'price', 'preview', )
    extra = 1

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.foto.url}" style="max-height: 100px;">')

    preview.short_description = 'просмотр'


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):

    list_display = ('title', )
    inlines = (ProductInline, )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.foto.url}" style="max-height: 200px;">')
    preview.short_description = 'фото'

    list_display = ('category', 'name', 'price')
    list_display_links = ('name', )
    list_editable = ('price', )
    list_filter = ('category', )
    search_fields = ('name', 'description', )

    fields = ('category', 'name', 'price', 'description', 'foto', 'id_foto_vk', 'preview')

    readonly_fields = ('id_foto_vk', 'preview' )
