# Find My Study Group (Laurier)

A Django web app for Wilfrid Laurier students to create and join study groups.
- Sign up with a Laurier email (@mylaurier.ca or @wlu.ca)
- Create groups with course, room, meeting time, and topics
- Request to join groups; owners approve/deny
- List page shows most popular groups first (by approved members)
- Filter by topics and search
- Laurier-inspired purple & gold theme

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

> To pre-load courses later, add them via the admin or build a simple import script.
