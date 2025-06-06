from django.urls import path
from . import views

urlpatterns = [
    path('api/classes/', views.list_classes, name='list_classes'),
    path('api/book/', views.book_class, name='book_class'),
    path('api/bookings/', views.get_bookings, name='get_bookings'),
]