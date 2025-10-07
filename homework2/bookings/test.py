from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import Client

from .models import Movie, Seat, Booking


# -------------------------
# Unit tests (models)
# -------------------------
class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.movie = Movie.objects.create(
            title="Unit Movie",
            description="desc",
            release_date="2025-01-01",
            duration=120,
        )
        cls.seat = Seat.objects.create(seat_number="A1")

    def test_movie_fields(self):
        self.assertEqual(self.movie.title, "Unit Movie")
        self.assertEqual(self.movie.description, "desc")
        self.assertEqual(str(self.movie.release_date), "2025-01-01")
        self.assertEqual(self.movie.duration, 120)

    def test_seat_fields(self):
        self.assertEqual(self.seat.seat_number, "A1")

    def test_booking_create(self):
        booking = Booking.objects.create(
        movie=self.movie,
        seat=self.seat,
        booking_date=timezone.now(),   # <-- add this
        )
        self.assertEqual(booking.movie, self.movie)
        self.assertEqual(booking.seat, self.seat)
        self.assertIsNotNone(booking.booking_date)


# -------------------------
# Integration tests (API)
# -------------------------
class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.movie = Movie.objects.create(
            title="Sample Movie",
            description="Demo",
            release_date="2025-01-01",
            duration=120,
        )
        # Create 8 seats A1..A8
        for i in range(1, 9):
            Seat.objects.create(seat_number=f"A{i}")

    def test_list_movies(self):
        r = self.client.get("/api/movies/")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(isinstance(data, list))
        self.assertEqual(data[0]["title"], "Sample Movie")

    def test_list_seats_has_booked_flag(self):
        r = self.client.get("/api/seats/")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        # Should include "booked" boolean (all False initially)
        self.assertIn("booked", data[0])
        self.assertFalse(any(s["booked"] for s in data))

    def test_booking_flow_create_conflict_delete(self):
        # 1) Create a booking via the API
        r1 = self.client.post(
            "/api/bookings/",
            {
                "movie_id": self.movie.id,
                "seat_id": Seat.objects.get(seat_number="A1").id,
                # IMPORTANT: provide booking_date to satisfy current serializer
                "booking_date": timezone.now().isoformat(),
            },
            content_type="application/json",
        )
        self.assertEqual(r1.status_code, 201, r1.content)
        booking_id = r1.json()["id"]
        seat_id = r1.json()["seat"]["id"]

        # 2) Seats endpoint should now show that seat as booked
        r2 = self.client.get("/api/seats/")
        self.assertEqual(r2.status_code, 200)
        seats_by_id = {s["id"]: s for s in r2.json()}
        self.assertTrue(seats_by_id[seat_id]["booked"])

        # 3) Booking the same seat again should conflict (400)
        r3 = self.client.post(
            "/api/bookings/",
            {
                "movie_id": self.movie.id,
                "seat_id": seat_id,
                "booking_date": timezone.now().isoformat(),
            },
            content_type="application/json",
        )
        self.assertEqual(r3.status_code, 400)
        self.assertIn("Seat is already booked", r3.content.decode())

        # 4) Delete the booking
        r4 = self.client.delete(f"/api/bookings/{booking_id}/")
        self.assertEqual(r4.status_code, 204)

        # 5) Seat should be available again
        r5 = self.client.get("/api/seats/")
        self.assertFalse({s["id"]: s for s in r5.json()}[seat_id]["booked"])

        # 6) No bookings left
        r6 = self.client.get("/api/bookings/")
        self.assertEqual(r6.status_code, 200)
        self.assertEqual(len(r6.json()), 0)
