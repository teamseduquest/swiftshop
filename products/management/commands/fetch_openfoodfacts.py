from django.core.management.base import BaseCommand
from products.models import Product, Category
import requests, random, os, tempfile
from urllib.parse import urlparse
from django.core.files import File

API_BASE = "https://api.escuelajs.co/api/v1/products"

class Command(BaseCommand):
    help = "Fetch products from Platzi Fake Store API"

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=300, help='Max products to fetch')

    def handle(self, *args, **options):
        limit = options['limit']
        offset = 0
        total = 0

        def download_image(prod, url):
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmpf:
                        tmpf.write(resp.content)
                        tmpf.flush()
                        fname = os.path.basename(urlparse(url).path) or f"{prod.id}.jpg"
                        prod.image.save(fname, File(tmpf), save=True)
                        return True
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Image failed: {e}"))
            return False

        while total < limit:
            resp = requests.get(API_BASE, params={'offset': offset, 'limit': 100})
            if resp.status_code != 200:
                self.stdout.write(self.style.ERROR("Failed to fetch products"))
                break

            data = resp.json()
            if not data:
                break

            for item in data:
                title = item.get("title")
                desc = item.get("description", "")
                price = item.get("price", 0)
                cat_name = item.get("category", {}).get("name", "Misc")
                images = item.get("images", [])

                cat, _ = Category.objects.get_or_create(name=cat_name.title())

                prod, created = Product.objects.get_or_create(
                    name=title,
                    defaults={
                        "description": desc[:500],
                        "price": price,
                        "stock": random.randint(1, 20),
                        "category": cat
                    }
                )
                if (created or not prod.image) and images:
                    download_image(prod, images[0])

                total += 1
                self.stdout.write(f"{total}. {title}")

                if total >= limit:
                    break

            offset += len(data)

        self.stdout.write(self.style.SUCCESS(f"🛍️  Total products saved: {total}"))
