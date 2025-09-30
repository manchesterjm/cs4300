# CS4300/5300 – Homework 2: Movie Theater Booking

Live app: https://<your-render-subdomain>.onrender.com  
API root (DRF): https://<your-render-subdomain>.onrender.com/api/

## What this app does
- List movies
- Select seats to book (green = available, red = booked, blue = selected)
- Prevent double booking
- View & cancel “My Bookings”
- REST API for movies, seats, and bookings

## Local setup
```bash
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt

# Run dev server (SQLite)
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

AI Assistance Disclosure

I used ChatGPT (model: GPT-5 Thinking) as a coding assistant during this assignment. The tool was used to help me debug, reason about fixes, and draft small code snippets. I reviewed, edited, and tested all final code myself.

Specifically, AI assistance was used for:

Diagnosing URL issues (e.g., stray /proxy/8000 in links) and suggesting Django reverse()/url usage.

Clarifying booking logic so Seat availability is computed from Booking records (removing the stale Seat.booking_status flag).

Drafting/adjusting Django REST Framework serializers and view functions for:

GET /api/movies/, GET /api/seats/ (with booked flag), and GET/POST/DELETE /api/bookings/.

Writing/iterating unit & integration tests (model field checks, API booking flow, conflict prevention).

Troubleshooting database errors (e.g., NOT NULL constraint failed: bookings_booking.user_id) and migrations (making Booking.user nullable, adding defaults for Movie.release_date and duration).

Producing example cURL commands to verify the API (list, create, and delete bookings).

Helping configure Render deployment (gunicorn + WhiteNoise, DATABASE_URL, DJANGO_SECRET_KEY, DJANGO_DEBUG, Postgres setup) and advising where to run migrate.

Minor UI guidance (button states/colors and messages on conflict/cancel).

What I did independently:

Implemented the project structure, integrated suggestions, and wrote/fixed code to pass tests.

Ran all migrations and verified behavior locally and on Render.

Committed regularly, tagged milestones, and handled environment variables/secrets.

Performed manual and automated testing before submission.

No proprietary datasets or external codebases were used beyond standard libraries and documentation. All AI-generated suggestions were reviewed and adapted by me, and responsibility for the final implementation is my own.