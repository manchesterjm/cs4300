from django.urls import path, include
from bookings import views as bviews

# Base patterns (no prefix)
basepatterns = [
    path("", bviews.movie_list, name="movie_list"),
    path("movies/<int:movie_id>/book/", bviews.book_seat, name="book_seat"),
    path("bookings/", bviews.booking_history, name="booking_history"),
    path("bookings/<int:booking_id>/cancel/", bviews.cancel_booking, name="cancel_booking"),
]

# Serve both at root AND under /proxy/8000/ (when the proxy doesn't strip the prefix)
urlpatterns = [
    # Prefixed versions (so GET/POST to /proxy/8000/... resolve)
    path("proxy/8000/", include((basepatterns, "bookings"), namespace="prox")),
    # Root versions (so Django's own reversing still works normally)
    *basepatterns,
]
