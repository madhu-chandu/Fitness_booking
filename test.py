from django.urls import reverse
from rest_framework.test import APITestCase
from .models import FitnessClass
from django.utils import timezone

#sample test data
class BookingTests(APITestCase):
    def setUp(self):
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            date_time=timezone.now() + timezone.timedelta(days=1),
            instructor="Alice",
            available_slots=2
        )

    def test_booking_success(self):
        url = reverse('book_class')
        data = {
            'class_id': self.fitness_class.id,
            'client_name': 'Test User',
            'client_email': 'user@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_overbooking(self):
        self.fitness_class.available_slots = 0
        self.fitness_class.save()
        url = reverse('book_class')
        data = {
            'class_id': self.fitness_class.id,
            'client_name': 'Test User',
            'client_email': 'user@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No available slots', response.data['error'])