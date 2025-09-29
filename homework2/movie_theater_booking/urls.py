from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookings import views as bviews
from bookings.api import MovieViewSet, SeatViewSet, BookingViewSet

# Regular HTML pages (MVT)
basepatterns = [
    path("", bviews.movie_list, name="movie_list"),
    path("movies/<int:movie_id>/book/", bviews.book_seat, name="book_seat"),
    path("bookings/", bviews.booking_history, name="booking_history"),
    path("bookings/<int:booking_id>/cancel/", bviews.cancel_booking, name="cancel_booking"),
]

# REST API
router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="api-movie")
router.register(r"seats", SeatViewSet, basename="api-seat")
router.register(r"bookings", BookingViewSet, basename="api-booking")

api_patterns = [
    path("api/", include(router.urls)),
]

urlpatterns = [
    # Prefixed (proxy) versions so /proxy/8000/... works in your environment
    path("proxy/8000/", include((basepatterns, "bookings"), namespace="prox")),
    path("proxy/8000/", include((api_patterns, "api"), namespace="prox-api")),
    # Root versions (work locally without the proxy)
    *basepatterns,
    *api_patterns,
]
