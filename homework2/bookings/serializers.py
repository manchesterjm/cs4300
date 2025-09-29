from rest_framework import serializers
from .models import Movie, Seat, Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]

class SeatSerializer(serializers.ModelSerializer):
    # Ground truth: booked if there is a Booking row for this seat
    booked = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ["id", "seat_number", "booked"]  # no booking_status in the API

    def get_booked(self, obj):
        return Booking.objects.filter(seat_id=obj.id).exists()

class BookingSerializer(serializers.ModelSerializer):
    # Nice nested info on GET
    movie = MovieSerializer(read_only=True)
    seat = SeatSerializer(read_only=True)

    # Write-only on POST
    movie_id = serializers.IntegerField(write_only=True)
    seat_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ["id", "movie", "seat", "booking_date", "movie_id", "seat_id"]

    def validate(self, attrs):
        seat_id = attrs.get("seat_id")
        # Seat must exist
        seat = Seat.objects.filter(id=seat_id).first()
        if seat is None:
            raise serializers.ValidationError({"seat_id": "Seat not found."})
        # Must not already be booked (ground truth)
        if Booking.objects.filter(seat_id=seat_id).exists():
            raise serializers.ValidationError({"seat_id": "Seat is already booked."})
        return attrs
