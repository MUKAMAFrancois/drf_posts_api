from rest_framework.test import APITestCase
from django.urls import reverse




class TestPosts(APITestCase):
    
    def test_get_posts(self):
        response=self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code,200)
