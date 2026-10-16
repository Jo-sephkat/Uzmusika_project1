from django.db import models
from django.contrib.auth.models import User
import uuid

UNIVERSITIES = [
    ("University of Zimbabwe", "University of Zimbabwe"),
    ("NUST — Bulawayo", "NUST — Bulawayo"),
    ("Midlands State University", "Midlands State University"),
    ("Chinhoyi University of Technology", "Chinhoyi University of Technology"),
    ("Africa University", "Africa University"),
    ("Harare Institute of Technology", "Harare Institute of Technology"),
]

CATEGORIES = [
    ("Textbooks", "Textbooks"),
    ("Electronics", "Electronics"),
    ("Fashion", "Fashion"),
    ("Room & Living", "Room & Living"),
    ("Services", "Services"),
    ("Food & Snacks", "Food & Snacks"),
]

CATEGORY_ICONS = {
    "Textbooks": "📚",
    "Electronics": "💻",
    "Fashion": "👟",
    "Room & Living": "🛏️",
    "Services": "🛠️",
    "Food & Snacks": "🍱",
}

CONDITIONS = [
    ("New", "New"),
    ("Like new", "Like new"),
    ("Used", "Used"),
]

PAYMENT_CHOICES = [
    ('ecocash', 'EcoCash'),
    ('innbucks', 'InnBucks'),
    ('onemoney', 'OneMoney'),
    ('zipit', 'ZIPIT / Bank transfer'),
    ('cash', 'Cash on campus'),
]

class Profile(models.Model):
    ROLE_CHOICES = [
        ('vendor', 'Seller / Vendor'),
        ('buyer', 'Buyer'),
        ('both', 'Both (Buyer & Seller)'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='buyer')
    university = models.CharField(max_length=100, choices=UNIVERSITIES, default='University of Zimbabwe')
    store_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_email_confirmed = models.BooleanField(default=True)
    email_confirmation_token = models.UUIDField(default=uuid.uuid4)
    
    def display_name(self):
        if self.store_name:
            return self.store_name
        if self.user.first_name:
            return f"{self.user.first_name} {self.user.last_name}".strip()
        return self.user.username

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()}) - {self.university}"


class Product(models.Model):
    vendor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2) # US$
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    icon = models.CharField(max_length=10, default='📦')
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORIES, default='Textbooks')
    condition = models.CharField(max_length=50, choices=CONDITIONS, default='Used')
    university = models.CharField(max_length=100, choices=UNIVERSITIES, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def effective_university(self):
        return self.university or (self.vendor.university if self.vendor else "University of Zimbabwe")

    @property
    def display_icon(self):
        if self.icon and self.icon != '📦':
            return self.icon
        return CATEGORY_ICONS.get(self.category, '📦')

    def __str__(self):
        return f"{self.name} (US${self.price})"


class Service(models.Model):
    vendor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100, default='Services')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDER_STATUS = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='ecocash')
    payment_number = models.CharField(max_length=100, blank=True) # Phone/wallet number or note
    order_reference = models.CharField(max_length=32, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Pending')

    def save(self, *args, **kwargs):
        if not self.order_reference:
            self.order_reference = f"UT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} ({self.order_reference}) - {self.buyer.username} - US${self.total_amount}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity}x {self.product.name} @ US${self.price}"
