import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Emarket.models import Profile, Product, UNIVERSITIES, CATEGORIES

class Command(BaseCommand):
    help = 'Seeds sample Zimbabwean campus marketplace data for UniTrade'

    def handle(self, *args, **options):
        # Create or get demo sellers
        vendors_data = [
            {
                "username": "tariro_books",
                "first_name": "Tariro",
                "last_name": "Moyo",
                "email": "tariro@uz.ac.zw",
                "store_name": "Tariro's Book Nook",
                "university": "University of Zimbabwe",
                "phone": "+263 77 123 4567",
                "address": "New Complex 3, Room 42, UZ Campus",
            },
            {
                "username": "campus_tech",
                "first_name": "Farai",
                "last_name": "Chirwa",
                "email": "tech@hit.ac.zw",
                "store_name": "CampusTech ZW",
                "university": "Harare Institute of Technology",
                "phone": "+263 71 987 6543",
                "address": "HIT Technology Hub, Belvedere",
            },
            {
                "username": "sole_society",
                "first_name": "Panashe",
                "last_name": "Ncube",
                "email": "panashe@msu.ac.zw",
                "store_name": "Sole Society",
                "university": "Midlands State University",
                "phone": "+263 78 456 1234",
                "address": "Main Campus Res 4, Gweru",
            },
            {
                "username": "res_essentials",
                "first_name": "Nyasha",
                "last_name": "Gumbo",
                "email": "res@nust.ac.zw",
                "store_name": "Res Room Essentials",
                "university": "NUST — Bulawayo",
                "phone": "+263 77 555 8899",
                "address": "Hostel B, NUST, Bulawayo",
            },
        ]

        vendor_profiles = {}
        for vd in vendors_data:
            user, created = User.objects.get_or_create(
                username=vd["username"],
                defaults={
                    "first_name": vd["first_name"],
                    "last_name": vd["last_name"],
                    "email": vd["email"],
                    "is_active": True,
                }
            )
            if created:
                user.set_password("pass1234")
                user.save()

            profile, _ = Profile.objects.get_or_create(
                user=user,
                defaults={
                    "role": "vendor",
                    "store_name": vd["store_name"],
                    "university": vd["university"],
                    "phone": vd["phone"],
                    "address": vd["address"],
                    "is_email_confirmed": True,
                }
            )
            profile.role = "vendor"
            profile.store_name = vd["store_name"]
            profile.university = vd["university"]
            profile.phone = vd["phone"]
            profile.address = vd["address"]
            profile.save()
            vendor_profiles[vd["username"]] = profile

        # Sample products
        sample_products = [
            {
                "name": "Engineering Mathematics Bundle (5 books)",
                "cat": "Textbooks",
                "price": 45.00,
                "cond": "Like new",
                "vendor_key": "tariro_books",
                "uni": "University of Zimbabwe",
                "icon": "📚",
                "desc": "Five core first-year engineering maths textbooks, lightly used with no missing pages. Great starter set covering calculus, linear algebra, differential equations, and vectors."
            },
            {
                "name": "Slim 14\" Laptop — 8GB/256GB SSD",
                "cat": "Electronics",
                "price": 320.00,
                "cond": "Used",
                "vendor_key": "campus_tech",
                "uni": "Harare Institute of Technology",
                "icon": "💻",
                "desc": "Reliable daily-driver laptop, battery holds a full day of lectures. Intel Core i5, backlit keyboard, original charger and laptop sleeve included."
            },
            {
                "name": "Minimal White Sneakers — UK 8",
                "cat": "Fashion",
                "price": 38.00,
                "cond": "Like new",
                "vendor_key": "sole_society",
                "uni": "Midlands State University",
                "icon": "👟",
                "desc": "Worn a handful of times, clean soles, true to size UK 8. Premium white leather look, perfect for campus walkabouts."
            },
            {
                "name": "Business Law Casebook (Latest Edition)",
                "cat": "Textbooks",
                "price": 28.00,
                "cond": "Used",
                "vendor_key": "tariro_books",
                "uni": "University of Zimbabwe",
                "icon": "📕",
                "desc": "Current curriculum edition, essential for commerce and law majors. Clean condition, some highlighting in chapters 1-3 only."
            },
            {
                "name": "Scientific Calculator — Exam Approved",
                "cat": "Electronics",
                "price": 15.00,
                "cond": "Used",
                "vendor_key": "campus_tech",
                "uni": "Harare Institute of Technology",
                "icon": "🧮",
                "desc": "Exam-council approved non-programmable model, works perfectly, new CR2032 battery fitted. Includes slide-on hard case."
            },
            {
                "name": "Res Room Starter Kit — Kettle, Lamp, Storage",
                "cat": "Room & Living",
                "price": 55.00,
                "cond": "New",
                "vendor_key": "res_essentials",
                "uni": "NUST — Bulawayo",
                "icon": "🛏️",
                "desc": "Everything to set up a res room in one go: 1.7L stainless electric kettle, adjustable LED desk lamp, and foldable underbed storage organizer."
            },
            {
                "name": "Statistics Tutoring — 1 Hour Session",
                "cat": "Services",
                "price": 8.00,
                "cond": "New",
                "vendor_key": "tariro_books",
                "uni": "University of Zimbabwe",
                "icon": "🧠",
                "desc": "One-on-one stats tutoring, online via Google Meet or in-person at UZ library. Regression analysis, probability distributions, SPSS & hypothesis testing."
            },
            {
                "name": "Home-Cooked Lunch Plate (weekdays)",
                "cat": "Food & Snacks",
                "price": 3.00,
                "cond": "New",
                "vendor_key": "res_essentials",
                "uni": "NUST — Bulawayo",
                "icon": "🍱",
                "desc": "Fresh sadza & beef relish / chicken stew plate with veggies, made daily at 12:30 PM. Order ahead and collect warm from res kitchen."
            },
            {
                "name": "Noise Cancelling Wireless Headphones",
                "cat": "Electronics",
                "price": 42.00,
                "cond": "Like new",
                "vendor_key": "campus_tech",
                "uni": "Harare Institute of Technology",
                "icon": "🎧",
                "desc": "Over-ear Bluetooth headphones with active noise cancelling. Great for library study sessions and blocking hostel noise. 30h battery life."
            },
            {
                "name": "Dorm Desk Fan (USB / Rechargeable)",
                "cat": "Room & Living",
                "price": 18.00,
                "cond": "New",
                "vendor_key": "res_essentials",
                "uni": "Chinhoyi University of Technology",
                "icon": "💨",
                "desc": "Quiet 3-speed oscillating desk fan with built-in rechargeable battery that runs up to 6 hours during power cuts."
            },
            {
                "name": "Graphic Design & Poster Printing Service",
                "cat": "Services",
                "price": 10.00,
                "cond": "New",
                "vendor_key": "campus_tech",
                "uni": "Africa University",
                "icon": "🎨",
                "desc": "Custom flyers, CV formatting, project presentation slides, and event banners designed fast with same-day digital delivery."
            },
            {
                "name": "Vintage Denim Jacket — Medium",
                "cat": "Fashion",
                "price": 25.00,
                "cond": "Used",
                "vendor_key": "sole_society",
                "uni": "Midlands State University",
                "icon": "🧥",
                "desc": "Oversized classic denim trucker jacket in medium wash. 100% durable cotton denim, great condition with no tears."
            }
        ]

        for p in sample_products:
            Product.objects.get_or_create(
                name=p["name"],
                vendor=vendor_profiles[p["vendor_key"]],
                defaults={
                    "category": p["cat"],
                    "price": p["price"],
                    "condition": p["cond"],
                    "university": p["uni"],
                    "icon": p["icon"],
                    "description": p["desc"],
                    "is_available": True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(sample_products)} UniTrade campus listings!'))
