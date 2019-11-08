from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from post.models import BlogPost
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler  = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user = User(username='user1', email='user1@test.com')
        user.set_password("testpwd")
        user.save()
        blog_post = BlogPost.objects.create(
                user=user,
                title='somerandomtitle',
                content='abcdefghijklmnopqrstuvwxyz'
                )

    def test_single_user(self):
        user_cnt = User.objects.count()
        self.assertEqual(user_cnt, 1)

    def test_single_post(self):
        post_cnt = BlogPost.objects.count()
        self.assertEqual(post_cnt, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse("api-post:post-create")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        data = {"title": "Randometest", "content": "the quick brown fox jumps over the lazy dog"}
        url = api_reverse("api-post:post-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_update_item(self):
        blog_post = BlogPost.objects.first()
        data = {"title": "updatetest", "content": "once again the quick brown fox jumps over the lazy dog"}
        url = blog_post.get_api_url()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_authorization(self):
        blog_post = BlogPost.objects.first()
        data = {"title": "updatetest", "content": "once again the quick brown fox jumps over the lazy dog"}
        url = blog_post.get_api_url()
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item_with_auth(self):
        data = {"title": "updatetest", "content": "once again the quick brown fox jumps over the lazy dog"}
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        url = api_reverse("api-post:post-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        user_obj = User.objects.create(username='test2')
        blog_post = BlogPost.objects.create(
                user=user_obj,
                title='test2title',
                content='abcdefghijklmnopqrstuvwxyz'
                )

        not_owner = User.objects.first()

        self.assertNotEqual(user_obj.username, not_owner.username)

        payload = payload_handler(not_owner)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        url = blog_post.get_api_url()
        data = {"title": "updatetest", "content": "once again the quick brown fox jumps over the lazy dog"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_user_login_and_update(self):
        data = {
            'username': 'user1',
            'password': 'testpwd'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            blog_post = BlogPost.objects.first()
            data = {"title": "updatetest", "content": "once again the quick brown fox jumps over the lazy dog"}
            url = blog_post.get_api_url()
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
