
from decimal import Decimal
from pathlib import Path
from django.conf import settings
from .models import Category, Product

DEMO_CATEGORIES = [
    ("Elektronika", "elektronika"),
    ("Telefonlar", "telefonlar"),
    ("Noutbuklar", "noutbuklar"),
    ("Audio", "audio"),
    ("Smart soatlar", "smart-soatlar"),
    ("Kiyimlar", "kiyimlar"),
    ("Poyabzallar", "poyabzallar"),
    ("Uy va mebel", "uy-va-mebel"),
    ("Go'zallik", "gozallik"),
    ("Gaming", "gaming"),
]

DEMO_PRODUCTS = [
    ("iPhone 15 Pro 256GB", "iphone-15-pro-256gb", "telefonlar", "Kuchli kamera va premium korpusli zamonaviy smartfon.", 12990000, 14990000, "products/iphone15.png", 18, 4.9),
    ("MacBook Air M3", "macbook-air-m3", "noutbuklar", "Yengil, tezkor va kundalik ishlar uchun qulay noutbuk.", 15990000, 17990000, "products/macbook.png", 9, 4.9),
    ("AirPods Pro 2", "airpods-pro-2", "audio", "Faol shovqinni kamaytirish va tiniq ovoz.", 2499000, 2899000, "products/airpods.png", 25, 4.8),
    ("Apple Watch Series 9", "apple-watch-series-9", "smart-soatlar", "Sport, aloqa va kundalik nazorat uchun aqlli soat.", 4299000, 4899000, "products/watch.png", 14, 4.8),
    ("Nike Air Max", "nike-air-max", "poyabzallar", "Qulay yurish va kundalik uslub uchun krossovka.", 1199000, 1499000, "products/sneaker.png", 31, 4.7),
    ("Sony Alpha Camera", "sony-alpha-camera", "elektronika", "Foto va video uchun yuqori sifatli kamera.", 10990000, 11990000, "products/camera.png", 7, 4.9),
    ("Premium Office Chair", "premium-office-chair", "uy-va-mebel", "Uzoq ishlash uchun ergonomik ofis kreslosi.", 1799000, 2199000, "products/chair.png", 16, 4.6),
    ("Premium Parfum", "premium-parfum", "gozallik", "Yoqimli va uzoq saqlanuvchi premium atir.", 699000, 849000, "products/perfume.png", 40, 4.8),
    ("Gaming Controller", "gaming-controller", "gaming", "Kompyuter va konsollar uchun qulay gamepad.", 599000, 749000, "products/gamepad.png", 22, 4.7),
    ("Kitchen Blender", "kitchen-blender", "uy-va-mebel", "Oshxona uchun kuchli va ixcham blender.", 489000, 599000, "products/blender.png", 27, 4.6),
    ("Urban Backpack", "urban-backpack", "kiyimlar", "Kundalik foydalanish va noutbuk uchun zamonaviy ryukzak.", 349000, 449000, "products/backpack.png", 35, 4.7),
    ("Smart Vacuum", "smart-vacuum", "uy-va-mebel", "Uy tozalash uchun zamonaviy changyutgich.", 2399000, 2799000, "products/vacuum.png", 11, 4.8),
]

def seed_demo_data():
    categories = {}
    for name, slug in DEMO_CATEGORIES:
        obj, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})
        if obj.name != name:
            obj.name = name
            obj.save(update_fields=["name"])
        categories[slug] = obj

    for name, slug, cat, description, price, old_price, image, stock, rating in DEMO_PRODUCTS:
        Product.objects.get_or_create(
            slug=slug,
            defaults={
                "category": categories[cat],
                "name": name,
                "description": description,
                "price": Decimal(price),
                "old_price": Decimal(old_price),
                "image": image,
                "stock": stock,
                "rating": Decimal(str(rating)),
                "is_active": True,
            },
        )
    return len(DEMO_PRODUCTS)
