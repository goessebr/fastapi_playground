De toepassing kan personen en organisaties beheren.
Een persoon kan deel uitmaken van meerdere organisaties, en een organisatie kan meerdere personen bevatten.

# Principes van de app-structuur

- Duidelijke scheiding van verantwoordelijkheden
- Elke methode heeft één concrete taak.
- Elke methode is zo op zichzelf eenvoudig te testen.
- Gebruik van dependency injection voor services in endpoints.
- dependencies kunnen veel maar mogen niet te complex worden om overzichtelijk te blijven in grote projecten:
  - ze leveren een instantie van een service of presenter
  - ze kunnen ook auth checks of andere cross-cutting concerns bevatten
  - ze mogen niet te veel logica bevatten
  - 
# App mapstructuur (kort)

REST API verkeer komt binnen via `app/api/` waar routers en endpoints gedefinieerd zijn.
HTML verkeer komt binnen via `app/web/` waar web-routes en server-side rendering logica zit.

De endpoints gebruiken services uit `app/services/` voor business logica.

De services spreken op data-laag helpers in `app/data/` voor database-interacties, 
interacties met ES en caching
Een onderdeel daarvan is de communicatie met de databank. We maken gebruik van dao's om
de concrete - eenvoudige en complexe - query's af te scheiden van de services.

 die op hun beurt data-laag helpers in `app/data/` kunnen aanroepen. 
Cross-cutting concerns zoals configuratie en logging zitten in `app/core/`. 
Domein- en API-excepties worden gedefinieerd in `app/exceptions/` en afgehandeld door FastAPI handlers. Integraties met externe systemen zitten in `app/infrastructure/`. Presenters in `app/presenters/` zorgen voor de conversie van domeinobjecten naar API-responses. Pydantic-schemas voor request/response validatie staan in `app/schemas/`. Security-gerelateerde helpers zijn te vinden in `app/security/`. De web-router en server-side rendering logica zit in `app/web/`. Statische bestanden en templates bevinden zich respectievelijk in `static/` en `templates/`. Diverse hulpfuncties staan in `utils/`.

Compacte opsomming van enkele belangrijke onderdelen voor het behandelen van een persoon request:
api/
- `api/` — HTTP-laag: routers, dependency wiring en endpoint-modules
  - `dependencies.py` — dependency providers (services, presenters, auth)
  - `router.py` — hoofdrouter die endpoints samenvoegt
  - `endpoints/` — concrete HTTP-endpoints
    - `persoon.py` — persoon-gerelateerde routes. Deze vertrouwen op de `persoon` service voor business logica en de `persoon` presenter voor response formatting.

data/
- `data/` — data-laag helpers en basisklassen
  - `db/` — database sessions, repositories en helpers
    - `dao/` - data access objects voor specifieke query's en interacties met de database
    - `models/` - ORM-modellen die de database-tabellen representeren
  - `search/` — ES

exceptions/
- `exceptions/` — domein- en API-excepties en handlers
  - `persoon.py` — persoon-specifieke exceptions

presenters/
- `presenters/` — presenteerlaag: converteert domeinobjecten naar API-vorm
  - `persoon.py` — presentatie/serialisatie voor `persoon` responses. 
  Afhankelijk van de context (object attributen en rechten gebruiker)

schemas/
- `schemas/` — Pydantic-modellen voor request/response validatie
  - `persoon.py` — persoon request/response schemas

security/
- `security/` — security-gerelateerde helpers per domein
  - `persoon.py` — persoon-gerelateerde security checks. Mag gebruiker de persoon-resource zien.

services/
- `services/` — business logic en orkestratie (gebruikt door endpoints via DI)
  - `persoon.py` — persoon-gerelateerde business logica (validatie, CRUD)


# App mapstructuur (volledig)

Compacte opsomming van de volledige inhoud van `app/` met één-regel beschrijvingen.

- `app/` — hoofdpackage voor applicatielogica (API, services, infra, schemas, enz.)

Top-level bestanden
- `__init__.py` — package marker
- `enums.py` — gedeelde enumeraties/constanten
- `main.py` — FastAPI entrypoint / ASGI-configuratie

api/
- `api/` — HTTP-laag: routers, dependency wiring en endpoint-modules
  - `__init__.py` — package marker
  - `dependencies.py` — dependency providers (services, presenters, auth)
  - `router.py` — hoofdrouter die endpoints samenvoegt
  - `endpoints/` — concrete HTTP-endpoints
    - `auth.py` — authenticatie endpoints / current-user dependency
    - `fastapi_oeutils.py` — kleine FastAPI helpers (bv. toegangchecks)
    - `health.py` — health-check endpoints
    - `organisatie.py` — organisatie-gerelateerde routes
    - `persoon.py` — persoon-gerelateerde routes

core/
- `core/` — cross-cutting concerns en configuratie
  - `config.py` — applicatieconfiguratie (settings)
  - `health.py` — health-check helpers
  - `logging.py` — logger configuratie / factory
  - `security.py` — security utilities (hashing, tokens, etc.)

data/
- `data/` — data-laag helpers en basisklassen
  - `__init__.py` — package marker
  - `base.py` — basisdata/ORM helper classes
  - `cache/` — caching-logica en adapters
  - `db/` — database sessions, repositories en helpers
  - `search/` — zoek/indexing gerelateerde code

exceptions/
- `exceptions/` — domein- en API-excepties en handlers
  - `__init__.py` — package marker
  - `auth.py` — auth-gerelateerde exceptions
  - `handlers.py` — FastAPI exception handlers (mapping naar HTTP-responses)
  - `organisatie.py` — organisatie-specifieke exceptions
  - `persoon.py` — persoon-specifieke exceptions

infrastructure/
- `infrastructure/` — integraties en externe systeemadapters
  - `clients.py` — algemene externe clients
  - `cache/` — cache-adapters / configuratie
  - `database/` — DB-connectoren / sessions / migratiehulp
  - `elasticsearch/` — ES-client en index-logica
  - `skos/` — SKOS / terminologie integratie
  - `storage/` — object storage / file adapters

presenters/
- `presenters/` — presenteerlaag: converteert domeinobjecten naar API-vriendelijke vormen
  - `persoon.py` — presentatie/serialisatie voor `persoon` responses

schemas/
- `schemas/` — Pydantic-modellen voor request/response validatie
  - `__init__.py` — package marker
  - `common.py` — gedeelde schema-componenten
  - `organisatie.py` — organisatie request/response schemas
  - `persoon.py` — persoon request/response schemas

security/
- `security/` — security-gerelateerde helpers per domein
  - `__init__.py` — package marker
  - `auth.py` — auth helpers (tokens, scopes)
  - `persoon.py` — persoon-gerelateerde security checks

services/
- `services/` — business logic en orkestratie (gebruikt door endpoints via DI)
  - `__init__.py` — package marker
  - `base.py` — basis service klasse / gedeelde logica
  - `organisatie.py` — organisatie-gerelateerde business logica
  - `persoon.py` — persoon-gerelateerde business logica (validatie, CRUD)

web/
- `web/` — web-specifieke router / server-side rendering
  - `router.py` — web-routes en template rendering

Overig
- `static/` — statische bestanden (JS/CSS/afbeeldingen)
- `templates/` — Jinja/HTML templates
- `utils/` — diverse hulpfuncties en kleine utilities

