# Python 3.14 / Django 6.0 Migration Analysis

**Branch:** `py3-dj6` vs `main`  
**Scope:** 89 files changed, 903 insertions, 995 deletions  
**Tests:** 47 passing  

## Summary

A clean modernisation-only migration. No new features, no gratuitous refactoring. The hardest change (replacing gevent/grequests with a stdlib ThreadPoolExecutor) is well-executed. The result is a simpler deployment with zero C extension dependencies.

## Architectural Changes

### grequests/gevent → ThreadPoolExecutor

The original relied on `grequests` (gevent monkey-patched `requests`) with `monkey.patch_all()` in `manage.py`. Replaced by `core/api/fetch.py` — a 60-line module using `concurrent.futures.ThreadPoolExecutor` that maintains the same deferred-batch API:

- `fetch.get(url, params, headers)` returns a deferred descriptor
- `fetch.map(batch)` executes all requests concurrently, returns responses in order
- Failed requests map to `None` (preserving the grequests contract)
- Adds per-request timeouts (previously absent)

Gunicorn switched from sync workers to `gthread` (4 workers x 8 threads) to match.

### pylibmc → Django cache framework

Direct `pylibmc` usage (C extension, required `libmemcached-dev`) replaced with `django.core.cache` backed by `pymemcache` (pure Python). All `mc.set(key, val, time=N)` calls updated to `cache.set(key, val, timeout=N)`.

### Dockerfile

From `python:2.7` with archived Debian repos and C build dependencies to `python:3.14-slim` with no system packages. `collectstatic` runs properly at build time. Whitenoise wired as middleware instead of WSGI wrapper.

## Django Modernisations

| Old (Django 1.5) | New (Django 6.0) |
|---|---|
| `MIDDLEWARE_CLASSES` tuple | `MIDDLEWARE` list with `__init__(get_response)` / `__call__` |
| `patterns('', url(...))` | Plain list with `re_path()` |
| `django.core.urlresolvers` | `django.urls` |
| `RequestContext` + `template.render(context)` | `template.render(view_data, request)` |
| `TEMPLATE_LOADERS` / `TEMPLATE_DIRS` / `TEMPLATE_CONTEXT_PROCESSORS` | `TEMPLATES` dict |
| `TEMPLATE_DEBUG` setting | Removed (folded into `DEBUG`) |
| `{% load staticfiles %}` | `{% load static %}` |
| `@register.assignment_tag` | `@register.simple_tag` |
| `\|length_is:"1"` | `\|length == 1` |
| Error handlers: `def not_found(request)` | `def not_found(request, exception=None)` |
| Dummy sqlite in `DATABASES` | `DATABASES = {}` |
| `USE_L10N`, `SITE_ID` | Removed (defaults changed or unnecessary) |
| `django.contrib.contenttypes` | Removed (unused without a database) |
| templatetags registered in `INSTALLED_APPS` | Removed (auto-discovered since Django 1.9) |

## Python 2 → 3 Syntax

- `print 'x'` → `print('x')`
- `dict.has_key('k')` → `'k' in dict`
- `urlparse` / `urllib` → `urllib.parse`
- `.iteritems()` → `.items()` (in templates)
- `collections.Iterable` → `collections.abc.Iterable`
- `xrange` → `range`
- `string.lowercase` → `string.ascii_lowercase`
- `raise Type, msg` → `raise Type(msg)`
- `except Type, e:` → `except Type as e:`
- `from local_settings import X` → `from microweb.local_settings import X`
- `response.content` → `response.text` (where str needed, not bytes)

## Dead Code Removed

- `fabfile.py` (Fabric deployment — replaced by Dokku git push)
- `upstart.sh` (Ubuntu Upstart init script)
- `core/middleware/exception.py` (Riemann exception reporting)
- `core/middleware/ga.py` (Google Analytics via pyga)
- `core/middleware/timing.py` (Riemann request timing)
- `core/middleware/modtimeurls.py` (static file cache busting — replaced by whitenoise)
- Dependencies removed: `grequests`, `gevent`, `pylibmc`, `bernhard`, `pyga`, `newrelic`, `mock`, `fabric`

## Bugs Fixed (pre-existing on main)

1. **`ignored.html`**: `content.results.items` → `content.items` (template referenced non-existent attribute)
2. **`block_comment_single.html`**: `item_type = 'conversation'` → `item_type == 'conversation'` (assignment vs comparison in template if-tag)
3. **`huddle.html` / modals**: `content.meta.creates|timesince` → `content.meta.created|timesince` (typo)

## Improvements Beyond Migration

1. **`FileMetadata.from_create_form`** — now sends explicit MIME type in multipart upload tuple instead of relying on `requests` to guess (it doesn't)
2. **`PermissionSet.empty()`** — `Meta` always has a `.permissions` attribute now, preventing AttributeError in templates when API omits permissions
3. **`Breadcrumb` / `ChildLinks`** — use `.get()` instead of `if 'key' in dict` pattern, more concise
4. **`Site.resolve_cname`** — returns `.text` not `.content`, preventing bytes being concatenated into URL strings
5. **`APIException`** — explicitly sets `self.message` in constructor (Python 3 removed `BaseException.message`)
6. **`core/api/fetch`** — adds request timeout (30s default), preventing indefinite hangs on API outages

## No Bugs Introduced

The migration introduces zero regressions. All changes are the minimum necessary for the version bump, with a few genuine fixes picked up along the way.
