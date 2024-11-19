from django.test import TestCase
from users.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

# Model Tests
class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='securepassword',
            email='testuser@example.com',
            role='student'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('securepassword'))
        self.assertEqual(self.user.role, 'student')

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), "testuser (student)")



# View Tests
class UserViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@example.com',
            role='admin'
        )
        self.student_user = User.objects.create_user(
            username='student',
            password='studentpassword',
            email='student@example.com',
            role='student'
        )
        self.teacher_user = User.objects.create_user(
            username='teacher',
            password='teacherpassword',
            email='teacher@example.com',
            role='teacher'
        )
        self.list_url = reverse('user-list')  

    def authenticate(self, user):
        """Authenticate a user using JWT"""
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_user_list_requires_authentication(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_creation(self):
        url = reverse('user-list')  
        self.authenticate(self.admin_user)
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'role': 'teacher'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertEqual(response.data['role'], 'teacher')

    def test_cache_on_user_list(self):
        self.authenticate(self.admin_user)
        response1 = self.client.get(self.list_url)
        response2 = self.client.get(self.list_url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
