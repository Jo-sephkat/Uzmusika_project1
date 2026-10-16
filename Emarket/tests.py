from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Profile, Order, OrderItem

class UniTradeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_student',
            password='password123',
            email='student@uz.ac.zw',
            first_name='Test',
            last_name='Student'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            role='vendor',
            store_name="Student Test Store",
            university='University of Zimbabwe',
            phone='+263771234567'
        )
        self.product = Product.objects.create(
            vendor=self.profile,
            name='Engineering Mathematics Volume 1',
            price=25.00,
            category='Textbooks',
            condition='Like new',
            university='University of Zimbabwe',
            description='Test textbook description'
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'UniTrade')
        self.assertContains(response, 'Engineering Mathematics Volume 1')

    def test_product_list_page(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marketplace')
        self.assertContains(response, 'Engineering Mathematics Volume 1')

    def test_product_detail_page(self):
        response = self.client.get(reverse('product_detail', kwargs={'pk': self.product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Engineering Mathematics Volume 1')
        self.assertContains(response, 'US$25.00')

    def test_cart_operations(self):
        # Add to cart
        response = self.client.post(reverse('add_to_cart', kwargs={'product_id': self.product.id}), {'quantity': 2})
        self.assertEqual(response.status_code, 302)

        # View cart
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Engineering Mathematics Volume 1')
        self.assertContains(response, 'US$50.00')

    def test_checkout_and_order(self):
        # Add item to cart
        self.client.post(reverse('add_to_cart', kwargs={'product_id': self.product.id}), {'quantity': 1})
        
        # Checkout POST
        response = self.client.post(reverse('make_purchase'), {
            'payment_method': 'ecocash',
            'payment_number': '0771234567',
            'buyer_name': 'Tatenda Moyo',
            'buyer_contact': 'tatenda@uz.ac.zw'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order Confirmed!')
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_vendor_profile_shows_seller_information(self):
        self.client.login(username='test_student', password='password123')
        response = self.client.get(reverse('vendor_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Seller Information')
        self.assertContains(response, 'Student Test Store')
        self.assertContains(response, 'student@uz.ac.zw')
        self.assertContains(response, 'Verified Student Seller')

    def test_buyer_profile_shows_customer_information(self):
        buyer = User.objects.create_user(username='buyer_student', password='password123', email='buyer@uz.ac.zw')
        Profile.objects.create(user=buyer, role='buyer', university='University of Zimbabwe')
        self.client.login(username='buyer_student', password='password123')
        response = self.client.get(reverse('buyer_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Customer Information')
        self.assertContains(response, 'buyer@uz.ac.zw')
        self.assertContains(response, 'Verified Campus Buyer')

    def test_account_settings_view(self):
        self.client.login(username='test_student', password='password123')
        response = self.client.get(reverse('account_settings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Name & Account Settings')
        self.assertContains(response, 'student@uz.ac.zw')

    def test_confirm_button_badge_in_vendor_dashboard(self):
        # Create an order
        order = Order.objects.create(
            buyer=self.user,
            total_amount=25.00,
            payment_method='ecocash',
            payment_number='0771234567',
            status='Pending'
        )
        OrderItem.objects.create(order=order, product=self.product, quantity=1, price=25.00)

        self.client.login(username='test_student', password='password123')
        response = self.client.get(reverse('vendor_dashboard'))
        self.assertEqual(response.status_code, 200)
        # Check confirm button with badge
        self.assertContains(response, 'btn-confirm-order')
        self.assertContains(response, 'badge-confirm')
        self.assertContains(response, 'Pending')

    def test_vendor_revenue_view(self):
        self.client.login(username='test_student', password='password123')
        response = self.client.get(reverse('vendor_revenue'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Revenue Summary')
        self.assertContains(response, 'Order Pipeline')
        self.assertContains(response, 'Sales Performance')

    def test_vendor_products_card_view(self):
        self.client.login(username='test_student', password='password123')
        response = self.client.get(reverse('vendor_products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'card-product')
        self.assertContains(response, 'Engineering Mathematics Volume 1')
        self.assertContains(response, 'US$25.00')

    def test_product_list_dropdown_filter(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<select name="uni"')
        self.assertContains(response, '<select name="cat"')
