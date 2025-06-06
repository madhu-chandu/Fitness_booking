import logging
import pytz
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer, BookingInputSerializer
from django.http import JsonResponse

logger = logging.getLogger(__name__)

# to list all available classes with slots
@api_view(['GET'])
def list_classes(request):
   if request.method == "GET":
        classes = FitnessClass.objects.all()
        data = []
        for c in classes:
            data.append({
                "id": c.id,
                "name": c.name,
                "instructor": c.instructor,
                "date_time": c.date_time.isoformat(),
                "available_slots": c.available_slots,
            })
        return JsonResponse(data, safe=False)

# to book a class
@api_view(['POST'])
def book_class(request):
    logger.info(f"Booking request received: {request.data}")
    serializer = BookingInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    class_id = serializer.validated_data['class_id']
    client_name = serializer.validated_data['client_name']
    client_email = serializer.validated_data['client_email']

    try:
        fitness_class = FitnessClass.objects.get(id=class_id)
    except FitnessClass.DoesNotExist:
        logger.warning(f"Class ID {class_id} not found")
        return Response({"error": "Fitness class not found."}, status=404) #if the class trying to book is not there prints error

    if fitness_class.available_slots <= 0:
        logger.warning(f"Class {class_id} overbooked")
        return Response({"error": "No available slots for this class."}, status=400)# alerts if slots are filled

    booking = Booking.objects.create(
        fitness_class=fitness_class,
        client_name=client_name,
        client_email=client_email
    )
    fitness_class.available_slots -= 1
    fitness_class.save()

    logger.info(f"Booking successful for {client_email} in class {class_id}") # confirmation message
    return Response(BookingSerializer(booking).data, status=201)

# to fetch classes booked by particular email
@api_view(['GET'])
def get_bookings(request):
    email = request.query_params.get('email')
    if not email:
        return Response({"error": "Email query parameter is required."}, status=400)

    bookings = Booking.objects.filter(client_email=email)
    return Response(BookingSerializer(bookings, many=True).data)

