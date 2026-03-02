from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

class BasicUserTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpass123"))