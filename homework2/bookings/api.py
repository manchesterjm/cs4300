from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

User = get_user_model()

def guest_user():
    user, _ = User.objects.get_or_create(username="guest", defaults={"is_active": False})
    return user

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all().order_by("title")
    serializer_class = MovieSerializer

class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Seat.objects.all().order_by("seat_number")
    serializer_class = SeatSerializer

class BookingViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Booking.objects.select_related("movie", "seat").order_by("-booking_date")
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        # Validate payload with serializer (ensures seat exists & not booked)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_id = serializer.validated_data["movie_id"]
        seat_id = serializer.validated_data["seat_id"]

        who = request.user if getattr(request.user, "is_authenticated", False) else guest_user()

        booking = Booking.objects.create(
            movie_id=movie_id,
            seat_id=seat_id,
            booking_date=timezone.now(),
            user=who,
        )

        out = self.get_serializer(booking)
        headers = {"Location": f"{request.build_absolute_uri().rstrip('/')}/{booking.id}/"}
        return Response(out.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
