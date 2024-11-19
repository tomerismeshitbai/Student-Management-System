from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from students.models import Student
from django.core.cache import cache
from datetime import date
from unittest.mock import patch

class StudentModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        
    def test_student_creation(self):
        student = Student.objects.create(user=self.user, dob=date(2000, 1, 1))
        
        self.assertEqual(student.user.username, 'testuser')
        self.assertEqual(student.dob, date(2000, 1, 1))
        self.assertIsNotNone(student.registration_date)
        
    def test_student_str_method(self):
        student = Student.objects.create(user=self.user, dob=date(2000, 1, 1))
        
        self.assertEqual(str(student), "testuser - testuser@example.com")

class StudentViewSetTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.student = Student.objects.create(user=self.user, dob=date(2000, 1, 1))
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
    def test_get_student_list(self):
        response = self.client.get('/api/students/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], 'testuser')
    
    def test_get_student_detail(self):
        response = self.client.get(f'/api/students/{self.student.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')
        
    @patch('django.core.cache.cache.delete') 
    def test_create_student(self, mock_cache_delete):
        new_user = User.objects.create_user(username='newuser', email='newuser@example.com', password='password123')
        data = {'user': new_user.id, 'dob': '2001-01-01'}
        
        response = self.client.post('/api/students/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        mock_cache_delete.assert_called_with(f"student_profile_{response.data['id']}")
        mock_cache_delete.assert_any_call("students_list")
    
    @patch('django.core.cache.cache.delete')  
    def test_update_student(self, mock_cache_delete):
        data = {'dob': '2002-02-02'}
        
        response = self.client.put(f'/api/students/{self.student.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        mock_cache_delete.assert_called_with(f"student_profile_{self.student.id}")
        mock_cache_delete.assert_any_call("students_list")
        
    @patch('django.core.cache.cache.delete')  
    def test_delete_student(self, mock_cache_delete):
        response = self.client.delete(f'/api/students/{self.student.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        mock_cache_delete.assert_called_with(f"student_profile_{self.student.id}")
        mock_cache_delete.assert_any_call("students_list")

