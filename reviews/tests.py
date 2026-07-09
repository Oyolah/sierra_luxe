from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from catalog.models import Category, Product
from .models import Review

User = get_user_model()


class ReviewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            price=100.00,
            stock=10,
            sizes='S,M,L',
            colors='Red,Blue',
            is_active=True
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='CUSTOMER'
        )

    def test_review_submission_authenticated(self):
        """Test authenticated user can submit a review"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            f'/reviews/product/{self.product.id}/add/',
            {'rating': 5, 'title': 'Great product', 'comment': 'I love it!'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(Review.objects.count(), 1)

    def test_review_submission_unauthenticated(self):
        """Test unauthenticated user cannot submit a review"""
        response = self.client.post(
            f'/reviews/product/{self.product.id}/add/',
            {'rating': 5, 'title': 'Great product', 'comment': 'I love it!'}
        )
        self.assertEqual(response.status_code, 302)

    def test_duplicate_review_prevention(self):
        """Test user cannot submit multiple reviews for same product"""
        self.client.login(username='testuser', password='testpass123')
        self.client.post(
            f'/reviews/product/{self.product.id}/add/',
            {'rating': 5, 'title': 'Great product', 'comment': 'I love it!'}
        )
        response = self.client.post(
            f'/reviews/product/{self.product.id}/add/',
            {'rating': 4, 'title': 'Still good', 'comment': 'Nice one'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Review.objects.count(), 1)

    def test_product_reviews_api(self):
        """Test reviews API returns reviews for a product"""
        Review.objects.create(
            product=self.product,
            customer=self.user,
            rating=5,
            title='Great',
            comment='Excellent product'
        )
        response = self.client.get(f'/reviews/product/{self.product.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['review_count'], 1)
        self.assertEqual(data['average_rating'], 5.0)

    def test_product_detail_shows_reviews(self):
        """Test product detail page includes reviews"""
        Review.objects.create(
            product=self.product,
            customer=self.user,
            rating=4,
            title='Good',
            comment='Good product'
        )
        response = self.client.get(f'/product/{self.product.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Good')

