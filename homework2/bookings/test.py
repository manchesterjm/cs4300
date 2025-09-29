from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Movie, Seat, Booking

# ---- Unit tests (models) -----------------------------------------------------

class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.movie = Movie.objects.create(
            title="Unit Movie",
            description="desc",
            release_date="2025-01-01",
            duration=120,
        )
        cls.seat = Seat.objects.create(seat_number="A1")  # booking_status ignored by app
        User = get_user_model()
        cls.user = User.objects.create_user(username="u1", password="x")

    def test_movie_fields(self):
        m = self.movie
        self.assertEqual(m.title, "Unit Movie")
        self.assertEqual(m.duration, 120)

    def test_seat_fields(self):
        s = self.seat
        self.assertEqual(s.seat_number, "A1")

    def test_booking_create(self):
        count_before = Booking.objects.count()
        b = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            booking_date=timezone.now(),
            user=self.user,
        )
        self.assertIsNotNone(b.id)
        self.assertEqual(Booking.objects.count(), count_before + 1)
        self.assertEqual(b.seat.seat_number, "A1")
        self.assertEqual(b.movie.title, "Unit Movie")


# ---- Integration tests (API) -------------------------------------------------

# We use the DRF test client for convenience
from rest_framework.test import APIClient

class APITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Data for tests: one movie, a few seats
        cls.movie = Movie.objects.create(
            title="API Movie",
            description="desc",
            release_date="2025-01-01",
            duration=120,
        )
        cls.seats = [
            Seat.objects.create(seat_number="A1"),
            Seat.objects.create(seat_number="A2"),
            Seat.objects.create(seat_number="A3"),
        ]
        # No need to create a user; API attaches to a 'guest' user automatically

    def setUp(self):
        self.client = APIClient()

    def test_list_movies(self):
        r = self.client.get("/api/movies/")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(isinstance(r.json(), list))
        self.assertIn("title", r.json()[0])

    def test_list_seats_has_booked_flag(self):
        r = self.client.get("/api/seats/")
        self.assertEqual(r.status_code, 200)
        first = r.json()[0]
        # serializer exposes: id, seat_number, booked
        self.assertIn("seat_number", first)
        self.assertIn("booked", first)
        self.assertIsInstance(first["booked"], bool)

    def test_booking_flow_create_conflict_delete(self):
        seat_id = self.seats[0].id

        # Initially, no bookings
        r0 = self.client.get("/api/bookings/")
        self.assertEqual(r0.status_code, 200)
        self.assertEqual(len(r0.json()), 0)

        # Create booking
        r1 = self.client.post(
            "/api/bookings/",
            {"movie_id": self.movie.id, "seat_id": seat_id},
            format="json",
        )
        self.assertEqual(r1.status_code, 201, r1.content)
        booking_id = r1.json()["id"]

        # Seats endpoint should show booked=True for that seat now
        r2 = self.client.get("/api/seats/")
        self.assertEqual(r2.status_code, 200)
        seat_rows = {s["id"]: s for s in r2.json()}
        self.assertTrue(seat_rows[seat_id]["booked"])

        # Trying to book same seat again -> 400 with validation error
        r3 = self.client.post(
            "/api/bookings/",
            {"movie_id": self.movie.id, "seat_id": seat_id},
            format="json",
        )
        self.assertEqual(r3.status_code, 400)
        self.assertIn("Seat is already booked", str(r3.content))

        # Delete the booking
        r4 = self.client.delete(f"/api/bookings/{booking_id}/")
        self.assertEqual(r4.status_code, 204)

        # Seats endpoint should show booked=False again
        r5 = self.client.get("/api/seats/")
        self.assertFalse({s["id"]: s for s in r5.json()}[seat_id]["booked"])

        # And bookings list should be empty again
        r6 = self.client.get("/api/bookings/")
        self.assertEqual(len(r6.json()), 0)
