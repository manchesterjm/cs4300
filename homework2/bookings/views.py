from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from django.contrib import messages

from .models import Movie, Seat, Booking

import os
from datetime import date


def _maybe_auto_seed():
    """
    Seed a default movie + seats on Render when DB is empty.
    Triggered only if AUTO_SEED=1 and there are no movies yet.
    Safe to call multiple times (idempotent).
    """
    if os.environ.get("AUTO_SEED") != "1":
        return

    if Movie.objects.exists():
        return

    m = Movie.objects.create(
        title="Sample Movie",
        description="Demo",
        release_date=date(2025, 1, 1),
        duration=120,
    )
    # Create A1..A8 seats if they don't exist
    for i in range(1, 9):
        Seat.objects.get_or_create(seat_number=f"A{i}")


def movie_list(request):
    _maybe_auto_seed()
    movies = Movie.objects.all().order_by("title")
    return render(request, "bookings/movie_list.html", {"movies": movies})


def book_seat(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # seats available / booked derived from Bookings (source of truth)
    seats = list(Seat.objects.all().order_by("seat_number"))
    booked_seat_ids = set(
        Booking.objects.filter(movie=movie).values_list("seat_id", flat=True)
    )

    if request.method == "POST":
        # seat ids come from checkboxes named "seats"
        selected_ids = request.POST.getlist("seats")
        try:
            selected_ids = [int(s) for s in selected_ids]
        except ValueError:
            selected_ids = []

        if not selected_ids:
            messages.error(request, "Please select at least one seat.")
            return redirect(reverse("book_seat", args=[movie.id]))

        # Which selected are already booked?
        already = [
            Seat.objects.get(id=sid).seat_number
            for sid in selected_ids
            if sid in booked_seat_ids
        ]
        if already:
            messages.error(
                request,
                "One or more selected seats are already booked: " + ", ".join(already),
            )
            return redirect(reverse("book_seat", args=[movie.id]))

        # Book atomically to avoid race conditions
        with transaction.atomic():
            # Re-check inside transaction
            current_booked = set(
                Booking.objects.select_for_update()
                .filter(movie=movie)
                .values_list("seat_id", flat=True)
            )
            conflict = [
                Seat.objects.get(id=sid).seat_number
                for sid in selected_ids
                if sid in current_booked
            ]
            if conflict:
                messages.error(
                    request,
                    "One or more selected seats are already booked: " + ", ".join(conflict),
                )
                return redirect(reverse("book_seat", args=[movie.id]))

            for sid in selected_ids:
                seat = Seat.objects.get(id=sid)
                Booking.objects.create(
                    movie=movie,
                    seat=seat,
                    booking_date=timezone.now(),
                )

        messages.success(request, f"Booked {len(selected_ids)} seat(s).")
        return redirect("booking_history")

    # GET: render page with availability flags
    seat_infos = []
    for seat in seats:
        seat_infos.append(
            {
                "id": seat.id,
                "number": seat.seat_number,
                "booked": seat.id in booked_seat_ids,
            }
        )

    return render(
        request,
        "bookings/seat_booking.html",
        {"movie": movie, "seats": seat_infos, "total_seats": len(seats)},
    )


def booking_history(request):
    bookings = (
        Booking.objects.select_related("movie", "seat")
        .order_by("-booking_date")
    )
    return render(request, "bookings/booking_history.html", {"bookings": bookings})


def cancel_booking(request, booking_id):
    if request.method != "POST":
        return redirect("booking_history")
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    messages.success(request, "Booking canceled.")
    return redirect("booking_history")
