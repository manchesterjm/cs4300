from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Movie, Seat, Booking

User = get_user_model()

def _guest_user():
    guest, _ = User.objects.get_or_create(username="guest", defaults={"is_active": False})
    return guest

def movie_list(request):
    movies = Movie.objects.all().order_by("title")
    return render(request, "bookings/movie_list.html", {"movies": movies})

def book_seat(request, movie_id: int):
    """
    Shows seats + books seats.
    IMPORTANT: Availability is computed from Booking table (not Seat.booking_status).
    """
    movie = get_object_or_404(Movie, pk=movie_id)
    seats = list(Seat.objects.all().order_by("seat_number"))

    # Ground truth: currently booked seat IDs
    booked_ids = set(Booking.objects.values_list("seat_id", flat=True))

    if request.method == "POST":
        raw = request.POST.get("seat_ids", "")
        ids = [s for s in raw.split(",") if s.strip()]
        try:
            requested_ids = {int(x) for x in ids}
        except ValueError:
            messages.error(request, "Invalid seat selection.")
            return redirect(reverse("book_seat", args=[movie.id]))

        if not requested_ids:
            messages.warning(request, "Please select at least one seat.")
            return redirect(reverse("book_seat", args=[movie.id]))

        # Re-check against current bookings to avoid race/mismatch
        booked_now = set(Booking.objects.values_list("seat_id", flat=True))
        already = sorted(requested_ids & booked_now)
        if already:
            names = ", ".join(Seat.objects.filter(id__in=already).values_list("seat_number", flat=True))
            messages.error(request, f"One or more selected seats are already booked: {names}.")
            return redirect(reverse("book_seat", args=[movie.id]))

        who = request.user if getattr(request.user, "is_authenticated", False) else _guest_user()
        for seat in Seat.objects.filter(id__in=requested_ids):
            Booking.objects.create(movie=movie, seat=seat, booking_date=timezone.now(), user=who)
            # Keep optional Seat.booking_status in sync if it exists
            if hasattr(seat, "booking_status"):
                seat.booking_status = True
                seat.save(update_fields=["booking_status"])

        messages.success(request, f"Booked {len(requested_ids)} seat(s).")
        return redirect(reverse("booking_history"))

    return render(
        request,
        "bookings/seat_booking.html",
        {
            "movie": movie,
            "seats": seats,
            "booked_ids": list(booked_ids),   # <-- pass ground-truth booked ids to template
        },
    )

def booking_history(request):
    bookings = Booking.objects.select_related("movie", "seat").order_by("-booking_date")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})

def cancel_booking(request, booking_id: int):
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect(reverse("booking_history"))

    b = get_object_or_404(Booking, pk=booking_id)
    seat = b.seat
    b.delete()

    # Keep optional Seat.booking_status in sync if present
    if hasattr(seat, "booking_status"):
        seat.booking_status = False
        seat.save(update_fields=["booking_status"])

    messages.success(request, f"Canceled booking for Seat {seat.seat_number}.")
    return redirect(reverse("booking_history"))
