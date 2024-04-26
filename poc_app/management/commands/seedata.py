import random
from faker import Faker
from django.core.management.base import BaseCommand
from ...models import Product

fake = Faker()

class Command(BaseCommand):
    help = 'Seed product data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding product data...'))
        self.seed_random_data(1000)
        self.stdout.write(self.style.SUCCESS('Successfully seeded product data.'))

    def seed_random_data(self, count):
        for _ in range(count):
            name = fake.company()
            description = fake.text()
            inventory = random.randint(0, 100)
            cost = round(random.uniform(10.0, 1000.0), 2)
            Product.objects.create(name=name, description=description, inventory=inventory, cost=cost)
