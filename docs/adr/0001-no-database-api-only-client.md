# ADR 0001: No database — API-only client

## Status

Accepted (inherited from original design)

## Context

Microweb is a Django web application that renders HTML for the Microcosm forum platform. All content (conversations, events, comments, profiles, sites) is owned by the Microcosm REST API. The question is whether microweb should maintain its own database or operate statelessly against the API.

Django conventionally assumes a database: its ORM, auth system, sessions, admin, and migration framework all depend on one. A Django project with `DATABASES = {}` is unusual and means none of those subsystems are available.

## Decision

Microweb has no database. `DATABASES = {}` in settings. All state is fetched from or written to the Microcosm API on every request. Authentication is handled via an `access_token` cookie validated by the API (no Django auth). The only local caching is memcached for CNAME/site resolution.

## Consequences

- No migrations, no ORM, no Django admin, no Django sessions.
- App `models.py` files are empty stubs — the "models" are in `core/api/resources.py` as API response wrappers.
- Tests subclass `SimpleTestCase` (nothing to flush or migrate).
- Authentication context is provided by custom middleware reading a cookie, not `django.contrib.auth`.
- The app is fully stateless and horizontally scalable — any instance can serve any request.
- A Microcosm API outage takes microweb down entirely; there is no local fallback.
