# import unittest, json, jwt, bcrypt

# from datetime      import datetime, timedelta
# from django.test   import TestCase, Client, TransactionTestCase
# from user.models   import User, Gender
# from my_settings   import SECRET, ALGORITHM
# from unittest.mock import patch, MagicMock

# class SignUpTestCase(TestCase):
#     def setUp(self):
#         User.objects.create(
#             id            = 1,
#             email         = 'wehuddling@gmail.com',
#             password      = 'asdfasdf',
#             phone_number  = '01012341234',
#             gender_id     = 1,
#             )

#     def tearDown(self):
#         Gender.objects.all().delete()
#         User.objects.all().delete()

#     def test_user_post_signup_success(self):
#         user = {
#                 'email'         : 'apple92gmail.com',
#                 'password'      : '123456a',
#                 'phone_number'  : '01012345678',
#                 'gender_id'     : 1,
#                 }
#         response = self.client.post('/user/signup', json.dumps(user), content_type='application/json')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json(),
#             {
#                 'MESSAGE':'SUCCESS'
#             }
#         )

#     def test_user_post_signup_email_exists_validation(self):
#         user = {
#                 'email'         : 'apple92gmail.com',
#                 'password'      : '123456a',
#                 'phone_number'  : '01012345678',
#                 'gender_id'     : 1,
#                 }
#         response = self.client.post('/user/signup', json.dumps(user), content_type='application/json')
#         self.assertEqual(response.status_code, 401)
#         self.assertEqual(response.json(),
#             {
#                 'MESSAGE' : 'ALREADY_EXISTS_EMAIL'
#             }
#         )

#     def test_user_post_signin_success(self):
#         user = {
#                 'email'    : 'applee24@gmail.com',
#                 'password' : '123456a'
#                 }

#         response = self.client.post('/user/signin', json.dumps(user), content_type='application/json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(),
#             {
#                 'access_token' : response.json()['access_token']
#             }
#         )