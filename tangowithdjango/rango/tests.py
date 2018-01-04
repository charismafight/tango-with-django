from django.test import TestCase

# Create your tests here.
from .models import Category


class CategoryMethodTest(TestCase):
    def test_ensure_views_are_positive(self):
        """
        ensure views are zero or positive
        """
        cat = Category("anything")
        cat.save()
        self.assertTrue(cat.visits >= 0)
