# Orderof.org Site Architecture

## Information Architecture

### Primary Navigation Structure
```
Orderof.org/
├── Home (/)
├── Books (/books)
│   ├── Popular Series (/books/popular)
│   ├── By Author (/books/authors)
│   ├── By Genre (/books/genres)
│   └── Search Results (/books/search)
├── Movies (/movies)
│   ├── Franchises (/movies/franchises)
│   ├── Cinematic Universes (/movies/universes)
│   ├── By Director (/movies/directors)
│   └── Search Results (/movies/search)
├── Series (/series)
│   ├── TV Shows (/series/tv)
│   ├── Web Series (/series/web)
│   ├── By Network (/series/networks)
│   └── Search Results (/series/search)
├── Anime (/anime)
│   ├── Popular Series (/anime/popular)
│   ├── By Studio (/anime/studios)
│   ├── By Genre (/anime/genres)
│   └── Search Results (/anime/search)
├── Games (/games)
│   ├── Game Series (/games/series)
│   ├── By Developer (/games/developers)
│   ├── By Platform (/games/platforms)
│   └── Search Results (/games/search)
├── Music (/music)
│   ├── Discographies (/music/artists)
│   ├── By Genre (/music/genres)
│   ├── Albums (/music/albums)
│   └── Search Results (/music/search)
└── Cars (/cars)
    ├── By Brand (/cars/brands)
    ├── By Generation (/cars/generations)
    ├── By Type (/cars/types)
    └── Search Results (/cars/search)
```

### Individual Item Pages
```
/[category]/[franchise-slug]/
├── Overview (default view)
├── Release Order (?order=release)
├── Chronological Order (?order=chronological)
├── Recommended Order (?order=recommended)
└── Custom Order (?order=custom) [Premium]
```

### User Account Pages
```
/account/
├── Dashboard (/account/dashboard)
├── My Lists (/account/lists)
├── Progress (/account/progress) [Premium]
├── Settings (/account/settings)
└── Subscription (/account/subscription)
```

## Database Schema

### Core Tables

#### Franchises
```sql
franchises (
  id: UUID PRIMARY KEY,
  name: VARCHAR(255) NOT NULL,
  slug: VARCHAR(255) UNIQUE NOT NULL,
  category: ENUM('books', 'movies', 'series', 'anime', 'games', 'music', 'cars'),
  description: TEXT,
  image_url: VARCHAR(500),
  created_at: TIMESTAMP,
  updated_at: TIMESTAMP,
  popularity_score: INTEGER DEFAULT 0
)
```

#### Items
```sql
items (
  id: UUID PRIMARY KEY,
  franchise_id: UUID REFERENCES franchises(id),
  title: VARCHAR(255) NOT NULL,
  slug: VARCHAR(255) NOT NULL,
  description: TEXT,
  release_date: DATE,
  image_url: VARCHAR(500),
  external_id: VARCHAR(100), -- API ID from TMDb, RAWG, etc.
  metadata: JSONB, -- Flexible storage for API-specific data
  created_at: TIMESTAMP,
  updated_at: TIMESTAMP
)
```

#### Orders
```sql
orders (
  id: UUID PRIMARY KEY,
  franchise_id: UUID REFERENCES franchises(id),
  order_type: ENUM('release', 'chronological', 'recommended', 'custom'),
  name: VARCHAR(255),
  description: TEXT,
  is_official: BOOLEAN DEFAULT false,
  created_by: UUID REFERENCES users(id),
  created_at: TIMESTAMP,
  updated_at: TIMESTAMP
)
```

#### Order Items
```sql
order_items (
  id: UUID PRIMARY KEY,
  order_id: UUID REFERENCES orders(id),
  item_id: UUID REFERENCES items(id),
  position: INTEGER NOT NULL,
  notes: TEXT,
  is_optional: BOOLEAN DEFAULT false
)
```

#### Affiliate Links
```sql
affiliate_links (
  id: UUID PRIMARY KEY,
  item_id: UUID REFERENCES items(id),
  platform: ENUM('amazon_uk', 'amazon_us', 'spotify', 'itunes', 'steam', 'other'),
  url: VARCHAR(500) NOT NULL,
  price: DECIMAL(10,2),
  currency: VARCHAR(3),
  is_active: BOOLEAN DEFAULT true,
  created_at: TIMESTAMP,
  updated_at: TIMESTAMP
)
```

### User Management Tables

#### Users
```sql
users (
  id: UUID PRIMARY KEY,
  email: VARCHAR(255) UNIQUE NOT NULL,
  password_hash: VARCHAR(255) NOT NULL,
  username: VARCHAR(50) UNIQUE,
  subscription_tier: ENUM('free', 'premium') DEFAULT 'free',
  subscription_expires: TIMESTAMP,
  created_at: TIMESTAMP,
  updated_at: TIMESTAMP
)
```

#### User Progress
```sql
user_progress (
  id: UUID PRIMARY KEY,
  user_id: UUID REFERENCES users(id),
  item_id: UUID REFERENCES items(id),
  status: ENUM('not_started', 'in_progress', 'completed'),
  rating: INTEGER CHECK (rating >= 1 AND rating <= 5),
  notes: TEXT,
  completed_at: TIMESTAMP,
  created_at: TIMESTAMP,
  updated_at: TIMESTAMP
)
```

## API Architecture

### Backend Framework: Flask (Python)
- **Reason:** Excellent for data-heavy applications, great API ecosystem
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Caching:** Redis for session management and API response caching
- **Search:** Elasticsearch for advanced search functionality

### API Endpoints Structure

#### Public Endpoints
```
GET /api/v1/franchises
GET /api/v1/franchises/{id}
GET /api/v1/franchises/{id}/orders
GET /api/v1/franchises/{id}/orders/{order_type}
GET /api/v1/categories/{category}/franchises
GET /api/v1/search?q={query}&category={category}
GET /api/v1/popular?category={category}&limit={limit}
```

#### User Endpoints (Authenticated)
```
POST /api/v1/auth/login
POST /api/v1/auth/register
GET /api/v1/user/profile
GET /api/v1/user/progress
POST /api/v1/user/progress
PUT /api/v1/user/progress/{item_id}
GET /api/v1/user/lists
POST /api/v1/user/lists
```

#### Admin Endpoints
```
POST /api/v1/admin/franchises
PUT /api/v1/admin/franchises/{id}
DELETE /api/v1/admin/franchises/{id}
POST /api/v1/admin/sync/{api_source}
```

### External API Integration

#### Data Sync Services
```python
# TMDb Integration
class TMDbService:
    def sync_movies(self, franchise_id)
    def sync_tv_shows(self, franchise_id)
    def get_movie_details(self, tmdb_id)

# RAWG Integration  
class RAWGService:
    def sync_games(self, franchise_id)
    def get_game_details(self, rawg_id)
    def get_game_series(self, series_name)

# Hardcover Integration
class HardcoverService:
    def sync_books(self, franchise_id)
    def get_book_details(self, book_id)
    def search_books(self, query)

# Spotify Integration
class SpotifyService:
    def sync_discography(self, artist_id)
    def get_album_details(self, album_id)
    def search_artists(self, query)

# CarAPI Integration
class CarAPIService:
    def sync_car_models(self, brand)
    def get_car_details(self, model_id)
    def get_generations(self, brand, model)
```

## Frontend Architecture

### Framework: React with Next.js
- **Reason:** Excellent SEO capabilities, server-side rendering
- **Styling:** Tailwind CSS for rapid development
- **State Management:** React Query for server state, Zustand for client state
- **UI Components:** Custom component library built on Headless UI

### Page Components Structure
```
src/
├── components/
│   ├── common/
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   ├── SearchBar.jsx
│   │   └── Navigation.jsx
│   ├── cards/
│   │   ├── FranchiseCard.jsx
│   │   ├── ItemCard.jsx
│   │   └── CategoryCard.jsx
│   ├── lists/
│   │   ├── OrderList.jsx
│   │   ├── ItemList.jsx
│   │   └── ProgressList.jsx
│   └── forms/
│       ├── SearchForm.jsx
│       ├── FilterForm.jsx
│       └── UserForm.jsx
├── pages/
│   ├── index.js (Homepage)
│   ├── [category]/
│   │   ├── index.js (Category page)
│   │   └── [franchise]/
│   │       └── index.js (Franchise page)
│   ├── search/
│   │   └── index.js (Search results)
│   └── account/
│       ├── dashboard.js
│       ├── lists.js
│       └── settings.js
├── hooks/
│   ├── useSearch.js
│   ├── useFranchise.js
│   └── useProgress.js
├── services/
│   ├── api.js
│   ├── auth.js
│   └── storage.js
└── utils/
    ├── constants.js
    ├── helpers.js
    └── validation.js
```

## SEO & Performance Strategy

### URL Structure
- **Clean URLs:** `/movies/marvel-cinematic-universe`
- **Canonical URLs:** Prevent duplicate content issues
- **Structured Data:** JSON-LD markup for rich snippets
- **Meta Tags:** Dynamic meta descriptions and titles

### Performance Optimizations
- **Image Optimization:** Next.js Image component with WebP
- **Code Splitting:** Route-based and component-based splitting
- **Caching Strategy:** 
  - Static assets: 1 year cache
  - API responses: 1 hour cache with stale-while-revalidate
  - Database queries: Redis caching for frequently accessed data

### Search Engine Optimization
- **Sitemap Generation:** Automated XML sitemap updates
- **Robot.txt:** Proper crawling directives
- **Page Speed:** Target Core Web Vitals scores
- **Mobile Optimization:** Mobile-first responsive design

## Security & Privacy

### Authentication & Authorization
- **JWT Tokens:** Secure token-based authentication
- **Password Security:** bcrypt hashing with salt
- **Rate Limiting:** API endpoint protection
- **CORS Configuration:** Proper cross-origin resource sharing

### Data Protection
- **GDPR Compliance:** User data rights and consent management
- **Data Encryption:** Sensitive data encryption at rest
- **Secure Headers:** CSP, HSTS, and other security headers
- **Input Validation:** Comprehensive input sanitization

This architecture provides a scalable, maintainable foundation for the Orderof.org platform while ensuring excellent user experience and performance.

