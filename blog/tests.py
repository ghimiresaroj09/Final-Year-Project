from django.test import TestCase
from .models import Category, BlogPost
from django.utils import timezone

class BlogTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Tips & Tricks')
        self.post = BlogPost.objects.create(
            title='Getting Started with Organic Farming',
            category=self.category,
            excerpt='Learn the basics of organic farming...',
            content='Organic farming is a sustainable practice...',
            author='John Doe'
        )
    
    def test_blog_post_creation(self):
        self.assertEqual(self.post.title, 'Getting Started with Organic Farming')
        self.assertEqual(self.post.slug, 'getting-started-with-organic-farming')
    
    def test_reading_time_calculation(self):
        self.assertGreaterEqual(self.post.reading_time, 1)
