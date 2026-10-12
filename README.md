# 📚 Booka

A backend-focused book discovery platform inspired by Goodreads and IMDb, built with **Django** and **Django REST Framework**.

Booka provides APIs for browsing books, exploring authors and genres, writing reviews, replying to reviews, liking reviews, and managing personal book collections.

> **Status:** Active development. Core APIs are implemented, but validation, concurrency handling, test coverage, and production configuration still need work.

## Implemented features

- Custom user model with an optional avatar.
- Registration, JWT login, token refresh, and authenticated profile updates.
- Book list and detail endpoints.
- Book search, filtering, ordering, and pagination.
- Author and genre endpoints.
- Review creation, replies, and recent reviews.
- Review like/unlike toggle with a unique user/review database constraint.
- Stored book average rating, recalculated through review signals.
- Public and private collections, with owner-scoped update and delete operations.
- Add/remove books in owned collections.
- Celery task for short-lived review notifications stored in Redis.
- Development seed command, model tests, and Docker Compose services.

## Stack

| Technology | Role |
| --- | --- |
| Python 3.13 | Version used by the Docker image |
| Django 6.0.1 | Application framework |
| Django REST Framework 3.16.1 | REST API |
| Simple JWT | JWT authentication |
| django-filter | Query parameter filtering |
| PostgreSQL 17 | Database in Docker Compose |
| Redis 7 | Cache and Celery broker in Docker Compose |
| Celery | Background tasks |
| Pillow | Image fields |
| pytest, pytest-django, factory-boy | Testing |
| Faker | Development seed data |

Dependencies are listed in [requirements.txt](requirements.txt). Some dependencies are not version-pinned yet.

## Project structure

```text
Booka/
├── core/
│   ├── manage.py
│   ├── booka/                 # Settings, root URLs, Celery, notification view
│   ├── account/
│   │   ├── api/               # Registration, JWT and profile endpoints
│   │   └── migrations/
│   └── book/
│       ├── api/               # Views, serializers, filters and pagination
│       ├── models/            # Authors, books, genres, reviews and collections
│       ├── migrations/
│       ├── management/commands/
│       ├── tests/
│       ├── signals.py
│       └── tasks.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Run with Docker Compose

The supplied Compose configuration runs Django, PostgreSQL, Redis, a Celery worker, and Celery Beat. The web container uses Django's development server.

### 1. Clone the repository

```bash
git clone https://github.com/HesamIrandoost/Booka.git
cd Booka
```

### 2. Create `.env` in the repository root

```dotenv
POSTGRES_DB=booka
POSTGRES_USER=booka
POSTGRES_PASSWORD=replace_with_a_local_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

The `.env` file is ignored by Git. Redis URLs are currently hardcoded in Django settings to use the Compose service hostname `redis`.

### 3. Start the database and Redis

```bash
docker compose up -d db redis
```

Wait until PostgreSQL reports that it is ready to accept connections. `depends_on` controls startup order but does not wait for database readiness.

### 4. Build, migrate, and create an administrator

```bash
docker compose build
docker compose run --rm web python core/manage.py migrate
docker compose run --rm web python core/manage.py createsuperuser
```

### 5. Start the application

```bash
docker compose up -d
```

- Books API: <http://127.0.0.1:8000/api/books/>
- Admin: <http://127.0.0.1:8000/admin/>

Useful commands:

```bash
docker compose logs -f web celery
docker compose down
```

## Run without Docker

Use Python 3.13 to match the Docker image. Provide a running PostgreSQL database and Redis instance.

```bash
python -m venv .venv
```

Activate the environment:

```bash
# Linux / macOS
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` with the same variables as above, but use your PostgreSQL hostname, such as `POSTGRES_HOST=127.0.0.1`. Create the database and user first.

For Redis running locally, change the cache location and Celery broker URL in `core/booka/settings.py` from hostname `redis` to `127.0.0.1`. These URLs are not currently configurable through `.env`.

```bash
python core/manage.py migrate
python core/manage.py createsuperuser
python core/manage.py runserver
```

Start a Celery worker in another terminal using the same virtual environment:

```bash
cd core
celery -A booka worker -l info
```

## API reference

Paths below are relative to the server root. Write operations marked authenticated require an access token.

| Method | Path | Access / behavior |
| --- | --- | --- |
| POST | `/api/auth/register/` | Public registration |
| POST | `/api/auth/login/` | Public; returns access and refresh tokens |
| POST | `/api/auth/refresh/` | Public; requires a refresh token |
| GET, PUT, PATCH | `/api/auth/me/` | Authenticated; current profile |
| GET | `/api/books/` | Public book list |
| GET | `/api/books/<slug>/` | Public book detail |
| GET, POST | `/api/books/<slug>/reviews/` | Public read; authenticated creation |
| POST | `/api/books/<slug>/reviews/<pk>/` | Authenticated; create a reply |
| GET | `/api/reviews/recent/` | Public; latest six active main reviews |
| POST | `/api/reviews/<pk>/like/` | Authenticated; toggle like, excluding own reviews |
| GET | `/api/authors/` | Public author list |
| GET | `/api/authors/<slug>/` | Public author detail |
| GET | `/api/genres/` | Public genre list |
| GET | `/api/genres/<pk>/` | Currently broken: route passes `pk`, view expects `slug` |
| GET, POST | `/api/collections/` | Public collections; authenticated creation |
| GET, POST | `/api/collections/user/` | Authenticated; own public and private collections |
| GET, PUT, PATCH, DELETE | `/api/collections/<pk>/` | Authenticated owner only |
| GET | `/api/collections/public/<pk>/` | Public collection detail |
| POST | `/api/collections/<pk>/add/<book_id>/` | Authenticated owner; add a book |
| DELETE | `/api/collections/<pk>/remove/<book_id>/` | Authenticated owner; remove a book |
| GET | `/notif/` | Reads and deletes the cached notification for the current user; authentication permission is not explicitly enforced yet |

### Authentication

Registration accepts `username`, `password`, `first_name`, and `last_name`. The password has a minimum length of eight characters; Django's configured password validators are not yet called by the registration serializer.

Login request:

```json
{
  "username": "reader",
  "password": "your_password"
}
```

Pass the access token on authenticated requests:

```http
Authorization: Bearer <access_token>
```

Refresh request:

```json
{
  "refresh": "<refresh_token>"
}
```

Profile updates accept `first_name`, `last_name`, and `avatar`. Image uploads require multipart form data.

### Search, filtering, and pagination

Books and authors use page-number pagination with **20 items per page**. Other list endpoints currently have no configured pagination, except recent reviews, which return at most six records.

```http
GET /api/books/?page=2
GET /api/books/?search=tolkien
GET /api/books/?genre=fantasy
GET /api/books/?author=author-slug
GET /api/books/?publisher=Publisher%20Name
GET /api/books/?ordering=-star
```

Book search covers title, author first/last name, and genre name. Supported ordering fields are `title`, `author`, `star`, and `published_date`; the default order is newest creation first.

Paginated responses contain `count`, `next`, `previous`, and `results`.

### Reviews and collections

Create a main review with:

```json
{
  "subject": "Worth reading",
  "text": "An engaging story with memorable characters.",
  "star": 5
}
```

The endpoint requires a rating from 1 to 5 and checks for an existing main review by the same user. Replies accept `text`; user, book, parent, and rating are assigned by the server.

Create a collection with `title`, optional `description` and `cover`, and `is_public`. Collections default to public. Books are read-only in the collection serializer; use the dedicated add/remove endpoints to change membership.

Review notification tasks store one message per user for 60 seconds. A newer message replaces the previous message; this is a temporary notification mechanism, not a persistent inbox. The Celery worker must be available to process tasks.

## Development seed data

**The seed command deletes existing reviews, collections, books, authors, genres, and all non-superuser accounts before generating data. Use a disposable development database only.**

```bash
# Docker
docker compose run --rm web python core/manage.py seed_data
```

```bash
# Local
python core/manage.py seed_data
```

The command generates 20 users plus authors, genres, books, reviews, replies, and collections. Generated users share the password `Test12345`.

## Tests

Run from `core/`, where `pytest.ini` is located:

```bash
cd core
pytest
```

Or through Docker:

```bash
docker compose run --rm -w /app/core web pytest
```

The configured PostgreSQL role must be able to create a test database. Current coverage includes model creation, author names, genres, and a basic rating average. API permissions, replies, moderation, concurrent requests, and background task failure paths are not covered yet. Some factories also need correction before broader use.

## Known limitations and next steps

- Fix the genre detail URL/view lookup mismatch.
- Exclude replies and inactive reviews from book rating calculations.
- Filter inactive reviews out of book detail responses.
- Validate that a reply's review belongs to the book identified by the URL.
- Add a database constraint for one main review per user/book and handle concurrent requests.
- Handle duplicate and non-ASCII titles when generating unique slugs.
- Remove the duplicate `ReviewSerializer` definition and repeated rating updates.
- Improve transaction boundaries and Celery failure handling around review creation.
- Complete nested query optimization for author and genre details.
- Add pagination to unbounded lists and simplify list response payloads.
- Expand model/API tests, repair factories, and add CI.
- Publish an API schema/documentation endpoint; `drf-yasg` is installed but no documentation route is configured.
- Add review update/delete APIs and persistent notifications if needed.

## Deployment status

The current configuration is intended for development: `DEBUG=True`, a hardcoded development secret key, empty `ALLOWED_HOSTS`, permissive CORS, and Django's development server.

Before production deployment, configure environment-specific settings, rotate the secret key, set allowed hosts and origins, disable debug, use a production application server, and configure static/media serving. Database readiness checks, deployment automation, and operational monitoring remain future work.

## Learning focus

Booka is a practical project for learning relational modeling, Django ORM, DRF validation and permissions, database constraints, transactions, query optimization, testing, and background processing. The goal is to develop a reliable API and understand the behavior of each component.

## License

[MIT](LICENSE) — Copyright © 2026 Hesam irandoost.
