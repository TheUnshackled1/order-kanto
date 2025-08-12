from django.core.management.base import BaseCommand
from menu.models import MenuItem
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create sample Filipino street food menu items'

    def handle(self, *args, **options):
        menu_items = [
            {
                'name': 'Kwek-Kwek',
                'description': 'Quail eggs coated in orange batter and deep-fried, served with a spicy vinegar dip.',
                'price': Decimal('15.00')
            },
            {
                'name': 'Fish Balls',
                'description': 'Deep-fried fish meatballs on sticks, served with sweet, spicy, or vinegar sauce.',
                'price': Decimal('10.00')
            },
            {
                'name': 'Siomai',
                'description': 'Steamed dumplings filled with ground pork and shrimp, served with soy sauce and calamansi.',
                'price': Decimal('25.00')
            },
            {
                'name': 'Isaw',
                'description': 'Grilled chicken or pork intestines on skewers, usually dipped in vinegar or spicy sauce.',
                'price': Decimal('20.00')
            },
            {
                'name': 'Balut',
                'description': 'Fertilized duck embryo boiled and eaten from the shell, often with salt or vinegar.',
                'price': Decimal('25.00')
            },
            {
                'name': 'Betamax',
                'description': 'Grilled chicken or pork blood cubes on skewers. Named after old Betamax tapes for its shape.',
                'price': Decimal('15.00')
            },
            {
                'name': 'Adidas',
                'description': 'Grilled chicken feet marinated in savory sauce.',
                'price': Decimal('20.00')
            },
            {
                'name': 'Isdang Prito',
                'description': 'Fried fish, often small varieties like galunggong, served with vinegar.',
                'price': Decimal('30.00')
            },
            {
                'name': 'Tempura',
                'description': 'Deep-fried battered vegetables or seafood, similar to Japanese tempura, served with sauce.',
                'price': Decimal('35.00')
            },
            {
                'name': 'Banana Cue',
                'description': 'Deep-fried caramelized saba bananas skewered on sticks.',
                'price': Decimal('15.00')
            },
            {
                'name': 'Turon',
                'description': 'Fried banana spring rolls with brown sugar and jackfruit filling.',
                'price': Decimal('12.00')
            },
            {
                'name': 'Dirty Ice Cream',
                'description': 'Local street ice cream, usually sold in cones or cups with different flavors like ube or mango.',
                'price': Decimal('20.00')
            },
            {
                'name': 'Chicharon',
                'description': 'Deep-fried pork rinds, crunchy and salty snack.',
                'price': Decimal('25.00')
            },
            {
                'name': 'Halo-Halo',
                'description': 'Shaved ice dessert mixed with various sweetened fruits, beans, jellies, topped with leche flan and ube.',
                'price': Decimal('45.00')
            },
            {
                'name': 'Sorbetes',
                'description': 'Traditional Filipino ice cream, made with coconut or carabao milk, sold from street carts.',
                'price': Decimal('25.00')
            },
            {
                'name': 'Mais con Yelo',
                'description': 'Sweet corn kernels mixed with shaved ice and milk, a refreshing dessert.',
                'price': Decimal('20.00')
            },
        ]

        created_count = 0
        for item_data in menu_items:
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                defaults={
                    'description': item_data['description'],
                    'price': item_data['price']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created menu item: {item.name} - ₱{item.price}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Menu item already exists: {item.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new menu items!')
        ) 