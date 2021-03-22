import unittest, json, jwt, bcrypt

# from my_settings import SECRET,ALGORITHM
# from datetime import datetime
# from django.test import TestCase, TransactionTestCase, Client
# from request.models import CourseRequest
# from product.models import Product

# # Create your tests here.
# class ProductListViewTest(TransactionTestCase):
#     def setUp(self):
#         Product.objects.create(
#             id = 1,
#             name = '테스트',
#             manufacture = '테스트',
#             unit_price = 1000,
#             stock = 1,
#             expiration_date = '20200101',
#             created_at = str(datetime.now()),
#             updated_at = str(datetime.now()),
#         )


#     def tearDown(self):
#         Product.objects.all().delete()

#     def test_course_list_view_get(self):
#         client = Client()
#         response  = client.get('/product/main', content_type='application/json')

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['results'])
