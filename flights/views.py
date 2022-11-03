from datetime import datetime
from rest_framework import generics
from flights import serializers
from flights.models import Booking, Flight

from rest_framework.generics import CreateAPIView 
from .serializers import FlightSerializer, BookingSerializer,BookingDetailsSerializer,UpdateBookingSerializer,RegisterSerializer,LoginSerializer,CreateFlightSerilazer 
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
class FlightsList(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class BookingsList(generics.ListAPIView):
    queryset = Booking.objects.filter(date__gte=datetime.today())
    serializer_class = BookingSerializer


class BookingDetails(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailsSerializer
    lookup_field = "id"
    lookup_url_kwarg = "booking_id"


class UpdateBooking(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = UpdateBookingSerializer
    lookup_field = "id"
    lookup_url_kwarg = "booking_id"


class CancelBooking(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "booking_id"


class BookFlight(generics.CreateAPIView):
    serializer_class = UpdateBookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, flight_id=self.kwargs["flight_id"])

# DRF Task3: Register View
class RegisterAPIView(CreateAPIView):
     serializer_class = RegisterSerializer 

# DRF Task4: create & login
class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.data
            return Response(valid_data,status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# DRF Task5: permissions
class CreateFlight(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = CreateFlightSerilazer
    permission_classes = [IsAuthenticated]
