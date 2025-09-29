from rest_framework import serializers
from .models import Movie, Seat, Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "seat_number", "booking_status"]

class BookingSerializer(serializers.ModelSerializer):
    # read-only nested objects (for GET responses)
    movie = MovieSerializer(read_only=True)
    seat = SeatSerializer(read_only=True)

    # write-only fields for POST
    movie_id = serializers.IntegerField(write_only=True)
    seat_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ["id", "movie", "seat", "booking_date", "movie_id", "seat_id"]

    def validate(self, attrs):
        # Ensure seat exists and isn't already booked
        seat_id = attrs.get("seat_id")
        from .models import Seat, Booking as B
        seat = Seat.objects.filter(id=seat_id).first()
        if seat is None:
            raise serializers.ValidationError({"seat_id": "Seat not found."})
        if B.objects.filter(seat_id=seat_id).exists():
            raise serializers.ValidationError({"seat_id": "Seat is already booked."})
        return attrs
