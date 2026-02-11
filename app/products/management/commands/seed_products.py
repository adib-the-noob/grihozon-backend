from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import (
    Brand,
    Manufacturer,
    Country,
    Category,
    Product,
    ProductVariant,
    Media,
    ProductType,
    Unit,
)
from decimal import Decimal
import random


class Command(BaseCommand):
    help = "Seed the database with sample product data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        with transaction.atomic():
            self.create_countries()
            self.create_manufacturers()
            self.create_brands()
            self.create_categories()
            self.create_product_types()
            self.create_units()
            self.create_products()

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))

    def create_countries(self):
        countries_data = [
            {"name": "Bangladesh", "iso_code": "BD"},
            {"name": "India", "iso_code": "IN"},
            {"name": "China", "iso_code": "CN"},
            {"name": "Japan", "iso_code": "JP"},
            {"name": "United States", "iso_code": "US"},
            {"name": "Germany", "iso_code": "DE"},
            {"name": "Thailand", "iso_code": "TH"},
            {"name": "Vietnam", "iso_code": "VN"},
            {"name": "South Korea", "iso_code": "KR"},
            {"name": "Australia", "iso_code": "AU"},
        ]

        for data in countries_data:
            Country.objects.get_or_create(iso_code=data["iso_code"], defaults=data)

        self.stdout.write(f"  Created {len(countries_data)} countries")

    def create_manufacturers(self):
        manufacturers_data = [
            # Food & Beverage Manufacturers
            "Pran Foods Ltd",
            "ACI Foods Ltd",
            "Square Food & Beverage Ltd",
            "Nestle Bangladesh Ltd",
            "Unilever Bangladesh Ltd",
            "Meghna Group of Industries",
            "Bombay Sweets & Co. Ltd",
            "Olympic Industries Ltd",
            "Akij Food & Beverage Ltd",
            "Danish Foods Ltd",
            # Electronics Manufacturers
            "Samsung Electronics",
            "Walton Hi-Tech Industries",
            "Singer Bangladesh Ltd",
            "Vision Electronics",
            "Transtec Limited",
            "Marcel",
            # Personal Care
            "Marico Bangladesh Ltd",
            "Kohinoor Chemical Company",
            "Keya Cosmetics Ltd",
            "Lily Cosmetics",
            # Home & Kitchen
            "RFL Group",
            "Bengal Plastic Ltd",
            "Hamko Corporation Ltd",
            "Partex Star Group",
        ]

        for name in manufacturers_data:
            Manufacturer.objects.get_or_create(name=name)

        self.stdout.write(f"  Created {len(manufacturers_data)} manufacturers")

    def create_brands(self):
        brands_data = [
            # Food & Beverage Brands
            "Pran",
            "Radhuni",
            "Fresh",
            "Aarong Dairy",
            "Milk Vita",
            "Ispahani",
            "Teer",
            "Pusti",
            "Mum",
            "Olympic",
            "Danish",
            "Bombay Sweets",
            "Mr. Noodles",
            "Cocola",
            "Nestle",
            "Maggi",
            "Nescafe",
            "Horlicks",
            # Personal Care Brands
            "Lux",
            "Dove",
            "Sunsilk",
            "Clear",
            "Parachute",
            "Vaseline",
            "Ponds",
            "Fair & Lovely",
            "Keya",
            "Tibet",
            # Electronics Brands
            "Walton",
            "Samsung",
            "Sony",
            "LG",
            "Vision",
            "Singer",
            "Marcel",
            "Transtec",
            "Sharp",
            "Philips",
            # Home & Kitchen Brands
            "RFL",
            "Bengal",
            "Hamko",
            "Partex",
            "Berger",
            "Asian Paints",
            "Butterfly",
            "Prestige",
            "Hawkins",
            # Others
            "Bata",
            "Apex",
            "Aarong",
            "Yellow",
            "Richman",
        ]

        for name in brands_data:
            Brand.objects.get_or_create(name=name)

        self.stdout.write(f"  Created {len(brands_data)} brands")

    def create_categories(self):
        # Main Categories with subcategories
        categories_structure = {
            "Groceries": [
                "Rice & Flour",
                "Oil & Ghee",
                "Spices & Masala",
                "Salt & Sugar",
                "Dal & Pulses",
                "Dry Fruits & Nuts",
            ],
            "Dairy & Eggs": [
                "Milk",
                "Cheese",
                "Butter & Margarine",
                "Yogurt",
                "Eggs",
                "Cream",
            ],
            "Beverages": [
                "Tea",
                "Coffee",
                "Soft Drinks",
                "Juice",
                "Energy Drinks",
                "Water",
            ],
            "Snacks & Biscuits": [
                "Biscuits",
                "Chips & Crisps",
                "Namkeen & Savory",
                "Chocolates",
                "Candies",
                "Cakes & Pastries",
            ],
            "Personal Care": [
                "Shampoo",
                "Soap",
                "Toothpaste",
                "Skin Care",
                "Hair Care",
                "Deodorant",
            ],
            "Baby Care": [
                "Diapers",
                "Baby Food",
                "Baby Skin Care",
                "Baby Bath",
                "Feeding Essentials",
            ],
            "Household": [
                "Cleaning Supplies",
                "Laundry",
                "Air Fresheners",
                "Kitchen Essentials",
                "Storage & Organization",
            ],
            "Frozen Foods": [
                "Frozen Meat",
                "Frozen Fish",
                "Frozen Vegetables",
                "Ice Cream",
                "Ready to Cook",
            ],
            "Fresh Produce": [
                "Vegetables",
                "Fruits",
                "Herbs & Seasonings",
            ],
            "Electronics": [
                "Mobile Accessories",
                "Kitchen Appliances",
                "Personal Gadgets",
                "Lighting",
            ],
        }

        count = 0
        for parent_name, children in categories_structure.items():
            parent, _ = Category.objects.get_or_create(name=parent_name, parent=None)
            count += 1

            for child_name in children:
                Category.objects.get_or_create(name=child_name, parent=parent)
                count += 1

        self.stdout.write(f"  Created {count} categories (hierarchical)")

    def create_product_types(self):
        types_data = [
            "FMCG",
            "Electronics",
            "Fresh",
            "Frozen",
            "Packaged",
            "Liquid",
            "Perishable",
            "Non-Perishable",
        ]

        for name in types_data:
            ProductType.objects.get_or_create(name=name)

        self.stdout.write(f"  Created {len(types_data)} product types")

    def create_units(self):
        units_data = [
            {"name": "kg", "base_unit": "gm", "multiplier_to_base": Decimal("1000")},
            {"name": "gm", "base_unit": "gm", "multiplier_to_base": Decimal("1")},
            {"name": "L", "base_unit": "ml", "multiplier_to_base": Decimal("1000")},
            {"name": "ml", "base_unit": "ml", "multiplier_to_base": Decimal("1")},
            {"name": "pcs", "base_unit": "pcs", "multiplier_to_base": Decimal("1")},
            {"name": "pack", "base_unit": "pcs", "multiplier_to_base": Decimal("1")},
            {"name": "dozen", "base_unit": "pcs", "multiplier_to_base": Decimal("12")},
            {"name": "box", "base_unit": "pcs", "multiplier_to_base": Decimal("1")},
        ]

        for data in units_data:
            Unit.objects.get_or_create(name=data["name"], defaults=data)

        self.stdout.write(f"  Created {len(units_data)} units")

    def create_products(self):
        # Get references
        brands = list(Brand.objects.all())
        manufacturers = list(Manufacturer.objects.all())
        countries = list(Country.objects.all())
        categories = list(
            Category.objects.filter(parent__isnull=False)
        )  # Only subcategories
        product_types = list(ProductType.objects.all())
        units = list(Unit.objects.all())

        products_data = [
            # Groceries - Rice & Flour
            {
                "name": "Miniket Rice Premium",
                "name_bd": "মিনিকেট চাল প্রিমিয়াম",
                "description": {
                    "features": ["Premium quality", "Long grain", "Aromatic"],
                    "origin": "Local",
                },
                "brand": "Teer",
                "category": "Rice & Flour",
                "manufacturer": "Meghna Group of Industries",
                "variants": [
                    {
                        "sku": "RICE-MIN-1KG",
                        "unit": "kg",
                        "unit_value": 1,
                        "mrp": 85,
                        "selling_price": 80,
                    },
                    {
                        "sku": "RICE-MIN-5KG",
                        "unit": "kg",
                        "unit_value": 5,
                        "mrp": 420,
                        "selling_price": 395,
                    },
                    {
                        "sku": "RICE-MIN-10KG",
                        "unit": "kg",
                        "unit_value": 10,
                        "mrp": 830,
                        "selling_price": 780,
                    },
                    {
                        "sku": "RICE-MIN-25KG",
                        "unit": "kg",
                        "unit_value": 25,
                        "mrp": 2050,
                        "selling_price": 1950,
                    },
                ],
            },
            {
                "name": "Bashful Rice",
                "name_bd": "বাসমতী চাল",
                "description": {
                    "features": ["Imported", "Extra long grain", "Premium aroma"],
                    "origin": "India",
                },
                "brand": "Pran",
                "category": "Rice & Flour",
                "manufacturer": "Pran Foods Ltd",
                "variants": [
                    {
                        "sku": "RICE-BAS-1KG",
                        "unit": "kg",
                        "unit_value": 1,
                        "mrp": 180,
                        "selling_price": 165,
                    },
                    {
                        "sku": "RICE-BAS-5KG",
                        "unit": "kg",
                        "unit_value": 5,
                        "mrp": 880,
                        "selling_price": 820,
                    },
                ],
            },
            {
                "name": "Atta Flour",
                "name_bd": "আটা",
                "description": {
                    "features": ["Whole wheat", "Fresh ground"],
                    "usage": "Roti, Paratha",
                },
                "brand": "Teer",
                "category": "Rice & Flour",
                "manufacturer": "Meghna Group of Industries",
                "variants": [
                    {
                        "sku": "ATTA-TEE-1KG",
                        "unit": "kg",
                        "unit_value": 1,
                        "mrp": 68,
                        "selling_price": 62,
                    },
                    {
                        "sku": "ATTA-TEE-2KG",
                        "unit": "kg",
                        "unit_value": 2,
                        "mrp": 135,
                        "selling_price": 122,
                    },
                    {
                        "sku": "ATTA-TEE-5KG",
                        "unit": "kg",
                        "unit_value": 5,
                        "mrp": 330,
                        "selling_price": 305,
                    },
                ],
            },
            # Groceries - Oil & Ghee
            {
                "name": "Soybean Oil",
                "name_bd": "সয়াবিন তেল",
                "description": {
                    "features": ["Refined", "Cholesterol free", "Heart healthy"]
                },
                "brand": "Teer",
                "category": "Oil & Ghee",
                "manufacturer": "Meghna Group of Industries",
                "variants": [
                    {
                        "sku": "OIL-SOY-1L",
                        "unit": "L",
                        "unit_value": 1,
                        "mrp": 175,
                        "selling_price": 168,
                    },
                    {
                        "sku": "OIL-SOY-2L",
                        "unit": "L",
                        "unit_value": 2,
                        "mrp": 345,
                        "selling_price": 330,
                    },
                    {
                        "sku": "OIL-SOY-5L",
                        "unit": "L",
                        "unit_value": 5,
                        "mrp": 855,
                        "selling_price": 820,
                    },
                ],
            },
            {
                "name": "Mustard Oil Pure",
                "name_bd": "সরিষার তেল",
                "description": {
                    "features": ["Cold pressed", "Traditional", "Pungent aroma"]
                },
                "brand": "Radhuni",
                "category": "Oil & Ghee",
                "manufacturer": "Square Food & Beverage Ltd",
                "variants": [
                    {
                        "sku": "OIL-MUS-500ML",
                        "unit": "ml",
                        "unit_value": 500,
                        "mrp": 165,
                        "selling_price": 155,
                    },
                    {
                        "sku": "OIL-MUS-1L",
                        "unit": "L",
                        "unit_value": 1,
                        "mrp": 320,
                        "selling_price": 298,
                    },
                ],
            },
            {
                "name": "Pure Ghee",
                "name_bd": "খাঁটি ঘি",
                "description": {
                    "features": ["Premium quality", "Rich aroma", "Traditional process"]
                },
                "brand": "Aarong Dairy",
                "category": "Oil & Ghee",
                "manufacturer": "ACI Foods Ltd",
                "variants": [
                    {
                        "sku": "GHEE-AAR-200G",
                        "unit": "gm",
                        "unit_value": 200,
                        "mrp": 290,
                        "selling_price": 275,
                    },
                    {
                        "sku": "GHEE-AAR-400G",
                        "unit": "gm",
                        "unit_value": 400,
                        "mrp": 560,
                        "selling_price": 530,
                    },
                    {
                        "sku": "GHEE-AAR-900G",
                        "unit": "gm",
                        "unit_value": 900,
                        "mrp": 1200,
                        "selling_price": 1140,
                    },
                ],
            },
            # Groceries - Spices & Masala
            {
                "name": "Turmeric Powder",
                "name_bd": "হলুদ গুড়া",
                "description": {"features": ["Pure", "Rich color", "Aromatic"]},
                "brand": "Radhuni",
                "category": "Spices & Masala",
                "manufacturer": "Square Food & Beverage Ltd",
                "variants": [
                    {
                        "sku": "SPC-TUR-100G",
                        "unit": "gm",
                        "unit_value": 100,
                        "mrp": 55,
                        "selling_price": 50,
                    },
                    {
                        "sku": "SPC-TUR-200G",
                        "unit": "gm",
                        "unit_value": 200,
                        "mrp": 105,
                        "selling_price": 95,
                    },
                    {
                        "sku": "SPC-TUR-500G",
                        "unit": "gm",
                        "unit_value": 500,
                        "mrp": 250,
                        "selling_price": 230,
                    },
                ],
            },
            {
                "name": "Red Chili Powder",
                "name_bd": "মরিচ গুড়া",
                "description": {"features": ["Hot", "Vibrant red", "Pure"]},
                "brand": "Radhuni",
                "category": "Spices & Masala",
                "manufacturer": "Square Food & Beverage Ltd",
                "variants": [
                    {
                        "sku": "SPC-CHI-100G",
                        "unit": "gm",
                        "unit_value": 100,
                        "mrp": 75,
                        "selling_price": 68,
                    },
                    {
                        "sku": "SPC-CHI-200G",
                        "unit": "gm",
                        "unit_value": 200,
                        "mrp": 145,
                        "selling_price": 132,
                    },
                ],
            },
            {
                "name": "Garam Masala",
                "name_bd": "গরম মসলা",
                "description": {
                    "features": ["Blend of spices", "Aromatic", "Premium quality"]
                },
                "brand": "Pran",
                "category": "Spices & Masala",
                "manufacturer": "Pran Foods Ltd",
                "variants": [
                    {
                        "sku": "SPC-GAR-50G",
                        "unit": "gm",
                        "unit_value": 50,
                        "mrp": 65,
                        "selling_price": 58,
                    },
                    {
                        "sku": "SPC-GAR-100G",
                        "unit": "gm",
                        "unit_value": 100,
                        "mrp": 120,
                        "selling_price": 110,
                    },
                ],
            },
            # Dairy & Eggs
            {
                "name": "Fresh Milk Full Cream",
                "name_bd": "ফুল ক্রিম দুধ",
                "description": {
                    "features": ["Pasteurized", "Rich in calcium", "Fresh"]
                },
                "brand": "Aarong Dairy",
                "category": "Milk",
                "manufacturer": "ACI Foods Ltd",
                "variants": [
                    {
                        "sku": "MLK-AAR-500ML",
                        "unit": "ml",
                        "unit_value": 500,
                        "mrp": 55,
                        "selling_price": 52,
                    },
                    {
                        "sku": "MLK-AAR-1L",
                        "unit": "L",
                        "unit_value": 1,
                        "mrp": 105,
                        "selling_price": 100,
                    },
                ],
            },
            {
                "name": "Milk Vita Liquid Milk",
                "name_bd": "মিল্ক ভিটা",
                "description": {"features": ["UHT processed", "Long shelf life"]},
                "brand": "Milk Vita",
                "category": "Milk",
                "manufacturer": "ACI Foods Ltd",
                "variants": [
                    {
                        "sku": "MLK-VIT-250ML",
                        "unit": "ml",
                        "unit_value": 250,
                        "mrp": 30,
                        "selling_price": 28,
                    },
                    {
                        "sku": "MLK-VIT-500ML",
                        "unit": "ml",
                        "unit_value": 500,
                        "mrp": 55,
                        "selling_price": 52,
                    },
                    {
                        "sku": "MLK-VIT-1L",
                        "unit": "L",
                        "unit_value": 1,
                        "mrp": 100,
                        "selling_price": 95,
                    },
                ],
            },
            {
                "name": "Mozzarella Cheese",
                "name_bd": "মোজারেলা চিজ",
                "description": {
                    "features": ["Stretchy", "Perfect for pizza", "Mild flavor"]
                },
                "brand": "Aarong Dairy",
                "category": "Cheese",
                "manufacturer": "ACI Foods Ltd",
                "variants": [
                    {
                        "sku": "CHZ-MOZ-200G",
                        "unit": "gm",
                        "unit_value": 200,
                        "mrp": 280,
                        "selling_price": 260,
                    },
                    {
                        "sku": "CHZ-MOZ-500G",
                        "unit": "gm",
                        "unit_value": 500,
                        "mrp": 650,
                        "selling_price": 610,
                    },
                ],
            },
            {
                "name": "Farm Fresh Eggs",
                "name_bd": "ফার্ম ফ্রেশ ডিম",
                "description": {
                    "features": ["Free range", "High protein", "Fresh daily"]
                },
                "brand": "Fresh",
                "category": "Eggs",
                "manufacturer": "Pran Foods Ltd",
                "variants": [
                    {
                        "sku": "EGG-FRM-6PCS",
                        "unit": "pcs",
                        "unit_value": 6,
                        "mrp": 90,
                        "selling_price": 84,
                    },
                    {
                        "sku": "EGG-FRM-12PCS",
                        "unit": "dozen",
                        "unit_value": 12,
                        "mrp": 175,
                        "selling_price": 165,
                    },
                    {
                        "sku": "EGG-FRM-30PCS",
                        "unit": "pcs",
                        "unit_value": 30,
                        "mrp": 420,
                        "selling_price": 395,
                    },
                ],
            },
            # Beverages - Tea & Coffee
            {
                "name": "Ispahani Mirzapore Tea",
                "name_bd": "ইস্পাহানি মির্জাপুর চা",
                "description": {
                    "features": ["Premium blend", "Rich taste", "Aromatic"]
                },
                "brand": "Ispahani",
                "category": "Tea",
                "manufacturer": "Meghna Group of Industries",
                "variants": [
                    {
                        "sku": "TEA-ISP-100G",
                        "unit": "gm",
                        "unit_value": 100,
                        "mrp": 95,
                        "selling_price": 88,
                    },
                    {
                        "sku": "TEA-ISP-200G",
                        "unit": "gm",
                        "unit_value": 200,
                        "mrp": 185,
                        "selling_price": 172,
                    },
                    {
                        "sku": "TEA-ISP-400G",
                        "unit": "gm",
                        "unit_value": 400,
                        "mrp": 360,
                        "selling_price": 338,
                    },
                ],
            },
            {
                "name": "Nescafe Classic",
                "name_bd": "নেসক্যাফে ক্লাসিক",
                "description": {
                    "features": ["Instant coffee", "Rich aroma", "Premium quality"]
                },
                "brand": "Nescafe",
                "category": "Coffee",
                "manufacturer": "Nestle Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "COF-NES-50G",
                        "unit": "gm",
                        "unit_value": 50,
                        "mrp": 275,
                        "selling_price": 255,
                    },
                    {
                        "sku": "COF-NES-100G",
                        "unit": "gm",
                        "unit_value": 100,
                        "mrp": 520,
                        "selling_price": 485,
                    },
                    {
                        "sku": "COF-NES-200G",
                        "unit": "gm",
                        "unit_value": 200,
                        "mrp": 980,
                        "selling_price": 920,
                    },
                ],
            },
            # Beverages - Soft Drinks & Juice
            {
                "name": "Frooto Mango Juice",
                "name_bd": "ফ্রুটো আমের জুস",
                "description": {
                    "features": ["Real fruit juice", "No preservatives", "Refreshing"]
                },
                "brand": "Pran",
                "category": "Juice",
                "manufacturer": "Pran Foods Ltd",
                "variants": [
                    {
                        "sku": "JUI-FRO-250ML",
                        "unit": "ml",
                        "unit_value": 250,
                        "mrp": 30,
                        "selling_price": 28,
                    },
                    {
                        "sku": "JUI-FRO-500ML",
                        "unit": "ml",
                        "unit_value": 500,
                        "mrp": 55,
                        "selling_price": 50,
                    },
                    {
                        "sku": "JUI-FRO-1L",
                        "unit": "L",
                        "unit_value": 1,
                        "mrp": 100,
                        "selling_price": 92,
                    },
                ],
            },
            # Snacks & Biscuits
            {
                "name": "Lexus Cream Biscuit",
                "name_bd": "লেক্সাস ক্রিম বিস্কুট",
                "description": {
                    "features": ["Crunchy", "Cream filled", "Tea time snack"]
                },
                "brand": "Olympic",
                "category": "Biscuits",
                "manufacturer": "Olympic Industries Ltd",
                "variants": [
                    {
                        "sku": "BIS-LEX-75G",
                        "unit": "gm",
                        "unit_value": 75,
                        "mrp": 40,
                        "selling_price": 38,
                        "discount_type": "PERCENT",
                        "discount_value": 5,
                    },
                    {
                        "sku": "BIS-LEX-150G",
                        "unit": "gm",
                        "unit_value": 150,
                        "mrp": 75,
                        "selling_price": 70,
                        "discount_type": "PERCENT",
                        "discount_value": 7,
                    },
                ],
            },
            {
                "name": "Potato Crackers",
                "name_bd": "পটেটো ক্র্যাকার্স",
                "description": {"features": ["Crispy", "Salted", "Party snack"]},
                "brand": "Bombay Sweets",
                "category": "Chips & Crisps",
                "manufacturer": "Bombay Sweets & Co. Ltd",
                "variants": [
                    {
                        "sku": "CHP-POT-30G",
                        "unit": "gm",
                        "unit_value": 30,
                        "mrp": 20,
                        "selling_price": 18,
                    },
                    {
                        "sku": "CHP-POT-60G",
                        "unit": "gm",
                        "unit_value": 60,
                        "mrp": 40,
                        "selling_price": 35,
                    },
                    {
                        "sku": "CHP-POT-150G",
                        "unit": "gm",
                        "unit_value": 150,
                        "mrp": 90,
                        "selling_price": 82,
                    },
                ],
            },
            {
                "name": "Mr. Noodles Masala",
                "name_bd": "মিস্টার নুডলস মসলা",
                "description": {
                    "features": [
                        "Instant noodles",
                        "Spicy masala flavor",
                        "2-minute recipe",
                    ]
                },
                "brand": "Mr. Noodles",
                "category": "Namkeen & Savory",
                "manufacturer": "Pran Foods Ltd",
                "variants": [
                    {
                        "sku": "NDL-MRN-62G",
                        "unit": "gm",
                        "unit_value": 62,
                        "mrp": 20,
                        "selling_price": 18,
                    },
                    {
                        "sku": "NDL-MRN-4PACK",
                        "unit": "pack",
                        "unit_value": 4,
                        "mrp": 75,
                        "selling_price": 70,
                    },
                    {
                        "sku": "NDL-MRN-8PACK",
                        "unit": "pack",
                        "unit_value": 8,
                        "mrp": 145,
                        "selling_price": 135,
                    },
                ],
            },
            {
                "name": "Dairy Milk Chocolate",
                "name_bd": "ডেইরি মিল্ক চকোলেট",
                "description": {
                    "features": ["Milk chocolate", "Smooth & creamy", "Premium"]
                },
                "brand": "Nestle",
                "category": "Chocolates",
                "manufacturer": "Nestle Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "CHO-DAI-25G",
                        "unit": "gm",
                        "unit_value": 25,
                        "mrp": 50,
                        "selling_price": 48,
                    },
                    {
                        "sku": "CHO-DAI-50G",
                        "unit": "gm",
                        "unit_value": 50,
                        "mrp": 95,
                        "selling_price": 90,
                    },
                    {
                        "sku": "CHO-DAI-110G",
                        "unit": "gm",
                        "unit_value": 110,
                        "mrp": 200,
                        "selling_price": 185,
                    },
                ],
            },
            # Personal Care - Shampoo
            {
                "name": "Sunsilk Black Shine Shampoo",
                "name_bd": "সানসিল্ক ব্ল্যাক শাইন শ্যাম্পু",
                "description": {
                    "features": ["For black hair", "Adds shine", "Strengthens hair"]
                },
                "brand": "Sunsilk",
                "category": "Shampoo",
                "manufacturer": "Unilever Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "SHP-SUN-80ML",
                        "unit": "ml",
                        "unit_value": 80,
                        "mrp": 85,
                        "selling_price": 78,
                    },
                    {
                        "sku": "SHP-SUN-180ML",
                        "unit": "ml",
                        "unit_value": 180,
                        "mrp": 175,
                        "selling_price": 162,
                    },
                    {
                        "sku": "SHP-SUN-340ML",
                        "unit": "ml",
                        "unit_value": 340,
                        "mrp": 320,
                        "selling_price": 295,
                    },
                ],
            },
            {
                "name": "Clear Anti-Dandruff Shampoo",
                "name_bd": "ক্লিয়ার অ্যান্টি-ড্যান্ড্রাফ শ্যাম্পু",
                "description": {
                    "features": ["Anti-dandruff", "Cool menthol", "Deep clean"]
                },
                "brand": "Clear",
                "category": "Shampoo",
                "manufacturer": "Unilever Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "SHP-CLR-170ML",
                        "unit": "ml",
                        "unit_value": 170,
                        "mrp": 195,
                        "selling_price": 180,
                    },
                    {
                        "sku": "SHP-CLR-330ML",
                        "unit": "ml",
                        "unit_value": 330,
                        "mrp": 365,
                        "selling_price": 340,
                    },
                ],
            },
            # Personal Care - Soap
            {
                "name": "Lux Soft Touch Soap",
                "name_bd": "লাক্স সফট টাচ সোপ",
                "description": {"features": ["Moisturizing", "Fragrant", "Soft skin"]},
                "brand": "Lux",
                "category": "Soap",
                "manufacturer": "Unilever Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "SOP-LUX-100G",
                        "unit": "gm",
                        "unit_value": 100,
                        "mrp": 55,
                        "selling_price": 50,
                    },
                    {
                        "sku": "SOP-LUX-150G",
                        "unit": "gm",
                        "unit_value": 150,
                        "mrp": 80,
                        "selling_price": 72,
                    },
                    {
                        "sku": "SOP-LUX-3PACK",
                        "unit": "pack",
                        "unit_value": 3,
                        "mrp": 230,
                        "selling_price": 210,
                        "discount_type": "AMOUNT",
                        "discount_value": 20,
                    },
                ],
            },
            {
                "name": "Dove Beauty Bar",
                "name_bd": "ডাভ বিউটি বার",
                "description": {
                    "features": [
                        "1/4 moisturizing cream",
                        "Gentle cleansing",
                        "Soft smooth skin",
                    ]
                },
                "brand": "Dove",
                "category": "Soap",
                "manufacturer": "Unilever Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "SOP-DOV-100G",
                        "unit": "gm",
                        "unit_value": 100,
                        "mrp": 120,
                        "selling_price": 110,
                    },
                    {
                        "sku": "SOP-DOV-135G",
                        "unit": "gm",
                        "unit_value": 135,
                        "mrp": 155,
                        "selling_price": 142,
                    },
                ],
            },
            # Personal Care - Toothpaste
            {
                "name": "Pepsodent Germi Check",
                "name_bd": "পেপসোডেন্ট জার্মি চেক",
                "description": {
                    "features": ["Germ protection", "Fresh breath", "Strong teeth"]
                },
                "brand": "Ponds",
                "category": "Toothpaste",
                "manufacturer": "Unilever Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "TPS-PEP-50G",
                        "unit": "gm",
                        "unit_value": 50,
                        "mrp": 45,
                        "selling_price": 40,
                    },
                    {
                        "sku": "TPS-PEP-100G",
                        "unit": "gm",
                        "unit_value": 100,
                        "mrp": 85,
                        "selling_price": 78,
                    },
                    {
                        "sku": "TPS-PEP-200G",
                        "unit": "gm",
                        "unit_value": 200,
                        "mrp": 160,
                        "selling_price": 148,
                    },
                ],
            },
            # Personal Care - Skin Care
            {
                "name": "Parachute Coconut Oil",
                "name_bd": "প্যারাসুট নারকেল তেল",
                "description": {
                    "features": ["100% pure", "Nourishing", "For hair & skin"]
                },
                "brand": "Parachute",
                "category": "Hair Care",
                "manufacturer": "Marico Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "OIL-PAR-100ML",
                        "unit": "ml",
                        "unit_value": 100,
                        "mrp": 95,
                        "selling_price": 88,
                    },
                    {
                        "sku": "OIL-PAR-200ML",
                        "unit": "ml",
                        "unit_value": 200,
                        "mrp": 175,
                        "selling_price": 162,
                    },
                    {
                        "sku": "OIL-PAR-400ML",
                        "unit": "ml",
                        "unit_value": 400,
                        "mrp": 335,
                        "selling_price": 310,
                    },
                ],
            },
            {
                "name": "Vaseline Petroleum Jelly",
                "name_bd": "ভ্যাসলিন পেট্রোলিয়াম জেলি",
                "description": {
                    "features": ["Moisturizing", "Healing", "Multi-purpose"]
                },
                "brand": "Vaseline",
                "category": "Skin Care",
                "manufacturer": "Unilever Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "SKN-VAS-50G",
                        "unit": "gm",
                        "unit_value": 50,
                        "mrp": 75,
                        "selling_price": 68,
                    },
                    {
                        "sku": "SKN-VAS-100G",
                        "unit": "gm",
                        "unit_value": 100,
                        "mrp": 140,
                        "selling_price": 128,
                    },
                    {
                        "sku": "SKN-VAS-250G",
                        "unit": "gm",
                        "unit_value": 250,
                        "mrp": 325,
                        "selling_price": 298,
                    },
                ],
            },
            # Household - Cleaning
            {
                "name": "Vim Dishwashing Liquid",
                "name_bd": "ভিম ডিশওয়াশ লিকুইড",
                "description": {
                    "features": [
                        "Powerful degreasing",
                        "Lemon fresh",
                        "Gentle on hands",
                    ]
                },
                "brand": "RFL",
                "category": "Cleaning Supplies",
                "manufacturer": "Unilever Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "CLN-VIM-250ML",
                        "unit": "ml",
                        "unit_value": 250,
                        "mrp": 85,
                        "selling_price": 78,
                    },
                    {
                        "sku": "CLN-VIM-500ML",
                        "unit": "ml",
                        "unit_value": 500,
                        "mrp": 160,
                        "selling_price": 148,
                    },
                    {
                        "sku": "CLN-VIM-1L",
                        "unit": "L",
                        "unit_value": 1,
                        "mrp": 295,
                        "selling_price": 275,
                    },
                ],
            },
            {
                "name": "Surf Excel Detergent Powder",
                "name_bd": "সার্ফ এক্সেল ডিটারজেন্ট",
                "description": {
                    "features": ["Stain removal", "Bright whites", "Fresh fragrance"]
                },
                "brand": "RFL",
                "category": "Laundry",
                "manufacturer": "Unilever Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "DET-SRF-500G",
                        "unit": "gm",
                        "unit_value": 500,
                        "mrp": 95,
                        "selling_price": 88,
                    },
                    {
                        "sku": "DET-SRF-1KG",
                        "unit": "kg",
                        "unit_value": 1,
                        "mrp": 180,
                        "selling_price": 168,
                    },
                    {
                        "sku": "DET-SRF-2KG",
                        "unit": "kg",
                        "unit_value": 2,
                        "mrp": 350,
                        "selling_price": 325,
                    },
                ],
            },
            # Baby Care
            {
                "name": "MamyPoko Pants",
                "name_bd": "ম্যামিপোকো প্যান্ট",
                "description": {
                    "features": ["Extra absorbent", "Soft material", "Leak proof"]
                },
                "brand": "Fresh",
                "category": "Diapers",
                "manufacturer": "Unilever Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "DPR-MAM-S24",
                        "unit": "pack",
                        "unit_value": 24,
                        "mrp": 650,
                        "selling_price": 598,
                    },
                    {
                        "sku": "DPR-MAM-M20",
                        "unit": "pack",
                        "unit_value": 20,
                        "mrp": 650,
                        "selling_price": 598,
                    },
                    {
                        "sku": "DPR-MAM-L18",
                        "unit": "pack",
                        "unit_value": 18,
                        "mrp": 650,
                        "selling_price": 598,
                    },
                    {
                        "sku": "DPR-MAM-XL16",
                        "unit": "pack",
                        "unit_value": 16,
                        "mrp": 650,
                        "selling_price": 598,
                    },
                ],
            },
            {
                "name": "Cerelac Baby Food",
                "name_bd": "সেরেল্যাক বেবি ফুড",
                "description": {
                    "features": ["Nutritious", "Easy to digest", "Essential vitamins"]
                },
                "brand": "Nestle",
                "category": "Baby Food",
                "manufacturer": "Nestle Bangladesh Ltd",
                "variants": [
                    {
                        "sku": "BBY-CER-350G",
                        "unit": "gm",
                        "unit_value": 350,
                        "mrp": 550,
                        "selling_price": 510,
                    },
                    {
                        "sku": "BBY-CER-400G",
                        "unit": "gm",
                        "unit_value": 400,
                        "mrp": 620,
                        "selling_price": 575,
                    },
                ],
            },
            # More Groceries
            {
                "name": "Red Lentils (Masoor Dal)",
                "name_bd": "মসুর ডাল",
                "description": {
                    "features": ["Split red lentils", "High protein", "Quick cooking"]
                },
                "brand": "Pran",
                "category": "Dal & Pulses",
                "manufacturer": "Pran Foods Ltd",
                "variants": [
                    {
                        "sku": "DAL-MAS-500G",
                        "unit": "gm",
                        "unit_value": 500,
                        "mrp": 95,
                        "selling_price": 88,
                    },
                    {
                        "sku": "DAL-MAS-1KG",
                        "unit": "kg",
                        "unit_value": 1,
                        "mrp": 185,
                        "selling_price": 172,
                    },
                    {
                        "sku": "DAL-MAS-2KG",
                        "unit": "kg",
                        "unit_value": 2,
                        "mrp": 360,
                        "selling_price": 338,
                    },
                ],
            },
            {
                "name": "Chickpeas (Chola)",
                "name_bd": "ছোলা",
                "description": {
                    "features": ["Premium quality", "High fiber", "Versatile"]
                },
                "brand": "Teer",
                "category": "Dal & Pulses",
                "manufacturer": "Meghna Group of Industries",
                "variants": [
                    {
                        "sku": "DAL-CHO-500G",
                        "unit": "gm",
                        "unit_value": 500,
                        "mrp": 85,
                        "selling_price": 78,
                    },
                    {
                        "sku": "DAL-CHO-1KG",
                        "unit": "kg",
                        "unit_value": 1,
                        "mrp": 165,
                        "selling_price": 152,
                    },
                ],
            },
            {
                "name": "Iodized Salt",
                "name_bd": "আয়োডিনযুক্ত লবণ",
                "description": {"features": ["Iodized", "Pure", "Essential mineral"]},
                "brand": "Mum",
                "category": "Salt & Sugar",
                "manufacturer": "ACI Foods Ltd",
                "variants": [
                    {
                        "sku": "SLT-MUM-500G",
                        "unit": "gm",
                        "unit_value": 500,
                        "mrp": 25,
                        "selling_price": 22,
                    },
                    {
                        "sku": "SLT-MUM-1KG",
                        "unit": "kg",
                        "unit_value": 1,
                        "mrp": 45,
                        "selling_price": 42,
                    },
                ],
            },
            {
                "name": "White Sugar",
                "name_bd": "চিনি",
                "description": {"features": ["Refined", "Pure white", "Fine crystals"]},
                "brand": "Fresh",
                "category": "Salt & Sugar",
                "manufacturer": "Meghna Group of Industries",
                "variants": [
                    {
                        "sku": "SGR-WHT-500G",
                        "unit": "gm",
                        "unit_value": 500,
                        "mrp": 55,
                        "selling_price": 50,
                    },
                    {
                        "sku": "SGR-WHT-1KG",
                        "unit": "kg",
                        "unit_value": 1,
                        "mrp": 105,
                        "selling_price": 98,
                    },
                    {
                        "sku": "SGR-WHT-2KG",
                        "unit": "kg",
                        "unit_value": 2,
                        "mrp": 205,
                        "selling_price": 192,
                    },
                ],
            },
            {
                "name": "Cashew Nuts",
                "name_bd": "কাজু বাদাম",
                "description": {
                    "features": ["Premium whole", "Roasted", "Healthy snack"]
                },
                "brand": "Pran",
                "category": "Dry Fruits & Nuts",
                "manufacturer": "Pran Foods Ltd",
                "variants": [
                    {
                        "sku": "NUT-CAS-100G",
                        "unit": "gm",
                        "unit_value": 100,
                        "mrp": 250,
                        "selling_price": 230,
                    },
                    {
                        "sku": "NUT-CAS-250G",
                        "unit": "gm",
                        "unit_value": 250,
                        "mrp": 595,
                        "selling_price": 555,
                    },
                    {
                        "sku": "NUT-CAS-500G",
                        "unit": "gm",
                        "unit_value": 500,
                        "mrp": 1150,
                        "selling_price": 1080,
                    },
                ],
            },
            {
                "name": "Raisins",
                "name_bd": "কিসমিস",
                "description": {"features": ["Seedless", "Sweet", "Naturally dried"]},
                "brand": "Pran",
                "category": "Dry Fruits & Nuts",
                "manufacturer": "Pran Foods Ltd",
                "variants": [
                    {
                        "sku": "NUT-RAI-100G",
                        "unit": "gm",
                        "unit_value": 100,
                        "mrp": 85,
                        "selling_price": 78,
                    },
                    {
                        "sku": "NUT-RAI-250G",
                        "unit": "gm",
                        "unit_value": 250,
                        "mrp": 195,
                        "selling_price": 180,
                    },
                ],
            },
        ]

        product_count = 0
        variant_count = 0
        media_count = 0

        for product_data in products_data:
            # Find related objects
            brand = Brand.objects.filter(name=product_data["brand"]).first()
            category = Category.objects.filter(name=product_data["category"]).first()
            manufacturer = Manufacturer.objects.filter(
                name=product_data["manufacturer"]
            ).first()
            country = random.choice(countries) if countries else None
            product_type = random.choice(product_types) if product_types else None

            product, created = Product.objects.get_or_create(
                name=product_data["name"],
                defaults={
                    "name_bd": product_data.get("name_bd", ""),
                    "description": product_data.get("description", {}),
                    "brand": brand,
                    "category": category,
                    "manufacturer": manufacturer,
                    "origin_country": country,
                    "product_type": product_type,
                    "is_active": True,
                },
            )

            if created:
                product_count += 1

                # Create variants
                for v_data in product_data.get("variants", []):
                    unit = Unit.objects.filter(name=v_data.get("unit")).first()

                    variant, v_created = ProductVariant.objects.get_or_create(
                        sku=v_data["sku"],
                        defaults={
                            "product": product,
                            "unit": unit,
                            "unit_value": Decimal(str(v_data["unit_value"])),
                            "mrp": Decimal(str(v_data["mrp"])),
                            "selling_price": Decimal(str(v_data["selling_price"])),
                            "discount_type": v_data.get("discount_type"),
                            "discount_value": (
                                Decimal(str(v_data["discount_value"]))
                                if v_data.get("discount_value")
                                else None
                            ),
                            "stock_qty": random.randint(10, 500),
                            "is_active": True,
                        },
                    )
                    if v_created:
                        variant_count += 1

                # Create sample media for each product
                media_data = [
                    {
                        "media_type": "IMAGE",
                        "is_primary": True,
                        "sort_order": 0,
                        "caption": "Main Image",
                    },
                    {
                        "media_type": "IMAGE",
                        "is_primary": False,
                        "sort_order": 1,
                        "caption": "Product View",
                    },
                    {
                        "media_type": "IMAGE",
                        "is_primary": False,
                        "sort_order": 2,
                        "caption": "Packaging",
                    },
                ]

                for idx, m_data in enumerate(media_data):
                    media, m_created = Media.objects.get_or_create(
                        product=product,
                        sort_order=m_data["sort_order"],
                        defaults={
                            "media_url": f"https://placeholder.grihozon.com/products/{product.id}/image_{idx + 1}.jpg",
                            "media_type": m_data["media_type"],
                            "mime_type": "image/jpeg",
                            "caption": m_data["caption"],
                            "is_primary": m_data["is_primary"],
                        },
                    )
                    if m_created:
                        media_count += 1

        self.stdout.write(f"  Created {product_count} products")
        self.stdout.write(f"  Created {variant_count} product variants")
        self.stdout.write(f"  Created {media_count} media items")
