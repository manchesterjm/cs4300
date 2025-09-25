from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    # Use a positive integer for clarity; minutes noted in help_text
    duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Duration in minutes"
    )

    class Meta:
        ordering = ["title"]  # optional: keeps movie lists alphabetical

    def __str__(self):
        return self.title


class Seat(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("booked", "Booked"),
    ]

    seat_number = models.CharField(max_length=10)
    booking_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="available",
    )

    class Meta:
        ordering = ["seat_number"]  # optional: makes seat listings tidy

    def __str__(self):
        return f"{self.seat_number} ({self.booking_status})"


class Booking(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent double-booking the same seat for the same movie
        unique_together = ("movie", "seat")
        ordering = ["-booking_date"]  # newest bookings first

    def __str__(self):
        return f"{self.user} → {self.movie} / {self.seat}"
