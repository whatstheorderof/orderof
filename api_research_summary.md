# API Research Summary

## Movies/Series: TMDb API
- **API Key:** Provided by user.
- **Access:** Requires API key for all requests.
- **Features:** Comprehensive data on movies, TV shows, actors, images. Supports searching, trending, and detailed information retrieval.
- **Documentation:** Well-documented with clear examples and guides.

## Books: Hardcover API (Goodreads API is deprecated for new users)
- **API Key:** Requires API key, obtained from account settings.
- **Access:** GraphQL API.
- **Features:** Access to book data, reviews, and user libraries. Same API used by their website and apps.
- **Limitations:** Currently in beta, subject to change. Rate-limited to 60 requests/minute. Tokens expire annually. Queries have max depth of 3 and limited to user's own data, public data, and followed users' data. Not for browser-side use.
- **Documentation:** Available on their website, with GraphQL console for testing.

## Music: Spotify API
- **API Key:** Requires client ID and client secret for authorization.
- **Access:** Web API for metadata, Web Playback SDK for playback control.
- **Features:** Access to artist, album, and show data, search, playback control, and library management (playlists, tracks).
- **Documentation:** Comprehensive documentation with concepts, tutorials, how-tos, and API reference.

## Games: RAWG.io API
- **API Key:** Provided by user.
- **Access:** Requires API key with every request.
- **Features:** Over 500,000 games, screenshots, ratings, developers, tags, publishers, people. Comprehensive game data including descriptions, genres, release dates, store links, ESRB-ratings, playtime, videos, Metacritic ratings, websites, system requirements, DLCs, and franchises.
- **Limitations:** Free plan for non-commercial projects, up to 20,000 requests/month, requires backlinks. Commercial plans available.
- **Documentation:** Available on their website with examples.

## Cars: CarAPI.app
- **API Key:** No fees, no signup for basic dataset. Pay when ready to go live.
- **Access:** REST + JSON API, documented in OpenAPI (Swagger/Redoc).
- **Features:** Over 90,000 vehicles (US, 1900-present) with year, make, model, submodel, trims, engine, transmission, mileage, color specifications. VIN lookup, license plate lookup, OBD-II codes. CSV data feed available.
- **Limitations:** Data primarily for US vehicles. Free tier for basic use.
- **Documentation:** Available on their website.

