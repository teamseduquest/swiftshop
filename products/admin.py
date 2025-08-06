from django.contrib import admin
from .models import Product, Category
from django.utils.html import format_html
import requests
from urllib.parse import urlparse
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
import os


import tempfile  # replace NamedTemporaryFile with this

def download_image_to_product(product_obj, image_url):
    try:
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Use tempfile instead of NamedTemporaryFile from Django
            with tempfile.NamedTemporaryFile(suffix=".jpg") as img_temp:
                img_temp.write(image_response.content)
                img_temp.flush()
                filename = os.path.basename(urlparse(image_url).path)
                product_obj.image.save(filename, File(img_temp), save=True)
    except Exception as e:
        print(f"❌ Error saving image: {e}")



# ✅ Admin action to fetch products and save images
@admin.action(description="📦 Fetch 100+ Products from DummyJSON API")
def fetch_products_from_dummyjson(modeladmin, request, queryset):
    url = 'https://dummyjson.com/products?limit=100'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()['products']
        for item in data:
            category_name = item.get('category', 'Uncategorized')
            category_obj, _ = Category.objects.get_or_create(name=category_name.title())

            product, created = Product.objects.update_or_create(
                name=item['title'],
                defaults={
                    'description': item['description'],
                    'price': item['price'],
                    'stock': item['stock'],
                    'category': category_obj,
                }
            )

            if created or not product.image:
                download_image_to_product(product, item.get('thumbnail'))

        modeladmin.message_user(request, "✅ Products fetched and images saved.")
    else:
        modeladmin.message_user(request, "❌ Failed to fetch from DummyJSON API", level='error')


# ✅ Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'image_tag')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    actions = [fetch_products_from_dummyjson]

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50"/>', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'


# ✅ Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
