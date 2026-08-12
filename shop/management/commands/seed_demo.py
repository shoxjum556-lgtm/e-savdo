from django.core.management.base import BaseCommand
from shop.demo_data import seed_demo_data

class Command(BaseCommand):
    help = "MEGA E-SAVDO demo kategoriyalar va mahsulotlarini yaratadi"

    def handle(self, *args, **options):
        count = seed_demo_data()
        self.stdout.write(self.style.SUCCESS(f"Demo ma'lumotlar tayyor: {count} ta mahsulot."))
