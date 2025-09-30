import datetime
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Give safe defaults so migrations won’t prompt again
    release_date = models.DateField(default=datetime.date(2025, 1, 1))
    duration = models.PositiveIntegerField(default=120)  # minutes

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Seat(models.Model):
    seat_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.seat_number


class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="bookings")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField()
    # Make user optional so anonymous bookings work in production
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("movie", "seat")  # prevent double-booking same seat/movie
        ordering = ["-booking_date"]

    def __str__(self):
        return f"{self.movie} - {self.seat}"
