from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from .models import Movie, Seat, Booking

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
        raw = request.POST.get("seat_ids", "")
        ids = [s for s in raw.split(",") if s]
        if not ids:
            messages.warning(request, "Please select at least one seat.")
            return redirect(reverse("book_seat", args=[movie.id]))

        wanted = list(Seat.objects.filter(id__in=ids))
        if len(wanted) != len(ids):
            messages.error(request, "One or more seats no longer exist.")
            return redirect(reverse("book_seat", args=[movie.id]))

        # Reject already-booked seats
        if any(s.booking_status for s in wanted):
            messages.error(request, "One or more selected seats are already booked.")
            return redirect(reverse("book_seat", args=[movie.id]))

        # Create bookings and mark seats booked
        for seat in wanted:
            Booking.objects.create(movie=movie, seat=seat, booking_date=timezone.now())
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
