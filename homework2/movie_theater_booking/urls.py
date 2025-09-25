from django.contrib import admin
from django.urls import path
from bookings import views as bviews

urlpatterns = [
    path("admin/", admin.site.urls),                     # not linked in UI, but harmless
    path("", bviews.movie_list, name="movie_list"),      # R: list movies
    path("movies/<int:movie_id>/book/", bviews.book_seat, name="book_seat"),  # C+U: create bookings / mark seats booked
    path("bookings/", bviews.booking_history, name="booking_history"),        # R: read booking history
    path("bookings/<int:booking_id>/cancel/", bviews.cancel_booking, name="cancel_booking"),  # D: delete a booking
]
