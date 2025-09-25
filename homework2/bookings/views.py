from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Movie, Seat, Booking

User = get_user_model()

def _guest_user():
    # Use (or create once) a disabled "guest" user for anon bookings
    guest, _ = User.objects.get_or_create(
        username="guest",
        defaults={"is_active": False}
    )
    return guest

def movie_list(request):
    movies = Movie.objects.all().order_by("title")
    return render(request, "bookings/movie_list.html", {"movies": movies})

def book_seat(request, movie_id: int):
    """
    Seat page + booking flow.
    NOTE: Seat has no FK to Movie in your schema, so seats are global.
    """
    movie = get_object_or_404(Movie, pk=movie_id)
    seats = Seat.objects.all().order_by("seat_number")

    if request.method == "POST":
        # Parse seat ids from hidden field, make them unique ints
        raw = request.POST.get("seat_ids", "")
        ids = [s for s in raw.split(",") if s.strip()]
        try:
            id_set = {int(x) for x in ids}
        except ValueError:
            messages.error(request, "Invalid seat selection.")
            return redirect(reverse("book_seat", args=[movie.id]))

        if not id_set:
            messages.warning(request, "Please select at least one seat.")
            return redirect(reverse("book_seat", args=[movie.id]))

        wanted = list(Seat.objects.filter(id__in=id_set))
        if len(wanted) != len(id_set):
            messages.error(request, "One or more selected seats no longer exist.")
            return redirect(reverse("book_seat", args=[movie.id]))

        # STRICT: treat only boolean True as booked
        already = [s for s in wanted if (s.booking_status is True)]
        if already:
            bad = ", ".join(s.seat_number for s in already)
            messages.error(request, f"One or more selected seats are already booked: {bad}.")
            return redirect(reverse("book_seat", args=[movie.id]))

        # Determine which user to attach
        who = request.user if getattr(request.user, "is_authenticated", False) else _guest_user()

        # Create bookings and mark seats booked
        for seat in wanted:
            Booking.objects.create(
                movie=movie,
                seat=seat,
                booking_date=timezone.now(),
                user=who,                      # <-- set the user (avoids NOT NULL error)
            )
            seat.booking_status = True
            seat.save(update_fields=["booking_status"])

        messages.success(request, f"Booked {len(wanted)} seat(s).")
        return redirect(reverse("booking_history"))

    return render(request, "bookings/seat_booking.html", {"movie": movie, "seats": seats})

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
    seat.booking_status = False
    seat.save(update_fields=["booking_status"])
    messages.success(request, f"Canceled booking for Seat {seat.seat_number}.")
    return redirect(reverse("booking_history"))
