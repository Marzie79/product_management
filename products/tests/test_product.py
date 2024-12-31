from django.test import TestCase
from django.urls import reverse

from products.tests.utilities import test_create_token
from products.models import Product


class ProductViewsTestCase(TestCase):
    """Test case for product views."""
    fixtures = ['account.json', 'product.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fixture_headers = f'Bearer {test_create_token(1, 2)}'
        cls.fixture_manager_headers = f'Bearer {test_create_token(2, 3)}'
        cls.product = Product.objects.first()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_product_list_view_green(self):
        """
        Test that the product list view returns a 200 status code and contains the product name.
        """
        response = self.client.get(reverse('product-list-create'),
                                   HTTP_AUTHORIZATION=self.fixture_headers)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_manager_list_view_green(self):
        """
        Test that the product list view for managers returns a 200 status code and contains the product name.
        """

        response = self.client.get(reverse('product-list-create'),
                                   HTTP_AUTHORIZATION=self.fixture_manager_headers)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_view_green(self):
        """
        Test that the product detail view returns a 200 status code and contains the product name.
        """
        response = self.client.get(
            reverse('product-detail', args=[self.product.id]),
            HTTP_AUTHORIZATION=self.fixture_headers,)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_manager_detail_view_green(self):
        """
        Test that the product detail view for managers returns a 200 status code and contains the product name.
        """
        response = self.client.get(
            reverse('product-detail', args=[self.product.id]),
            HTTP_AUTHORIZATION=self.fixture_manager_headers)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_create_view_green(self):
        """
        Test that the product create view returns a 201 status code and the product is created.
        """
        response = self.client.post(reverse('product-list-create'),
                                    HTTP_AUTHORIZATION=self.fixture_headers,
                                    data={'name': 'New Product',
                                          'total_price': 20.0,
                                          'quantity': 10,
                                          })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name='New Product').exists())

    def test_product_update_view_green(self):
        """
        Test that the product update view returns a 200 status code and the product is updated.
        """
        response = self.client.patch(reverse('product-detail', args=[self.product.id]),
                                     HTTP_AUTHORIZATION=self.fixture_headers,
                                     data={'name': 'Updated Product',
                                           'total_price': 15.0
                                           },
                                     content_type="application/json",)
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_product_delete_view_green(self):
        """
        Test that the product delete view returns a 204 status code and the product is deleted.
        """
        response = self.client.delete(
            reverse('product-detail', args=[self.product.id]),
            HTTP_AUTHORIZATION=self.fixture_headers,
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_product_force_delete_green(self):
        """
        Test that the product force delete functionality works correctly.
        """
        product = Product.objects.all().last()
        product_name = product.__str__()
        product.delete(force_delete=True)
        self.assertFalse(Product.all_objects.filter(
            name=product_name).exists())
