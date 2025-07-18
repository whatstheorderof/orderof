# OrderOf.org - Complete Website Documentation

## Project Overview

OrderOf.org is a comprehensive web platform that helps users discover the perfect viewing, reading, or playing order for their favorite franchises across multiple media types including movies, TV series, books, anime, games, music, and cars.

### Key Features

- **Multi-Media Support**: Covers movies, TV series, books, anime, games, music, and cars
- **Multiple Viewing Orders**: Release order, chronological order, and custom orders
- **Affiliate Integration**: Amazon UK/US affiliate links for monetization
- **API Integration**: Real-time data from TMDb (movies/TV) and RAWG (games)
- **Responsive Design**: Mobile-first design with Poppins font
- **Modern Tech Stack**: React frontend with Flask backend

## Architecture

### Frontend (React)
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS with shadcn/ui components
- **Font**: Poppins from Google Fonts
- **Icons**: Lucide React
- **State Management**: React hooks (useState, useEffect)

### Backend (Flask)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite for development
- **APIs**: TMDb API for movies/TV, RAWG API for games
- **CORS**: Enabled for frontend-backend communication

### Database Schema

#### Core Tables
1. **Franchises**: Main franchise information
2. **Items**: Individual movies, books, games, etc.
3. **Orders**: Different viewing/reading orders
4. **OrderItems**: Items within specific orders
5. **AffiliateLinks**: Monetization links

## API Endpoints

### Franchise Management
- `GET /api/franchises` - List all franchises
- `GET /api/franchises/{id}` - Get franchise details
- `GET /api/franchises/{id}/orders` - Get franchise orders
- `GET /api/franchises/{id}/items` - Get franchise items

### Admin Endpoints
- `POST /api/admin/sync/tmdb/movies` - Sync TMDb movie data
- `POST /api/admin/sync/popular` - Sync popular franchises
- `POST /api/admin/affiliate-links/generate-amazon` - Generate Amazon affiliate links

### Affiliate Management
- `POST /api/admin/items/{id}/affiliate-links` - Create affiliate link
- `PUT /api/admin/affiliate-links/{id}` - Update affiliate link
- `DELETE /api/admin/affiliate-links/{id}` - Delete affiliate link

## Component Structure

### Main Components
- **App.jsx**: Main application component with routing
- **Header.jsx**: Navigation header with search
- **Hero.jsx**: Landing page hero section
- **Footer.jsx**: Site footer with links
- **FranchiseDetail.jsx**: Detailed franchise view
- **CategorySection.jsx**: Category-based franchise listings

### UI Components
- **FranchiseCard.jsx**: Individual franchise display
- **ItemCard.jsx**: Individual item with affiliate links
- **AffiliateButton.jsx**: Affiliate link buttons

## Features Implemented

### 1. Franchise Discovery
- Browse by category (movies, books, games, etc.)
- Search functionality
- Trending/popular franchises section

### 2. Viewing Orders
- Release order (chronological by release date)
- Story chronological order
- Custom curated orders
- Position-based ordering with notes

### 3. Affiliate Monetization
- Amazon UK and US affiliate links
- Platform-specific buttons (Spotify, iTunes, Steam)
- Price display support
- Click tracking capability

### 4. Data Integration
- TMDb API for movie and TV data
- RAWG API for game data
- Automatic image and metadata fetching
- Rating and popularity scores

## Configuration

### Environment Variables
```bash
# TMDb API
TMDB_API_KEY=8b459b6f6aa0f76b7bf3fba33086cb81
TMDB_READ_ACCESS_TOKEN=eyJhbGciOiJIUzI1NiJ9...

# RAWG API
RAWG_API_KEY=e27f4f6149ec4c358472cfd6913e6d85

# Affiliate Tags
AMAZON_UK_TAG=orderof-21
AMAZON_US_TAG=orderof-20
```

### Database Configuration
- SQLite database stored in `src/database/app.db`
- Automatic table creation on first run
- Foreign key constraints enabled

## Deployment

### Local Development
1. Backend: `cd orderof_backend && source venv/bin/activate && python src/main.py`
2. Frontend: `cd orderof_frontend && pnpm run dev --host`

### Production Deployment
- Frontend: Build with `pnpm run build` and deploy static files
- Backend: Deploy Flask app with production WSGI server
- Database: Migrate to PostgreSQL for production

## Sample Data

The system includes sample data for popular franchises:

### Movies
- Star Wars (9 movies with release and chronological orders)
- Marvel Cinematic Universe
- Harry Potter
- The Lord of the Rings
- Fast & Furious

### TV Series
- Game of Thrones
- Breaking Bad
- Stranger Things
- The Office

### Games
- The Legend of Zelda
- Super Mario
- Call of Duty
- Grand Theft Auto

## Monetization Strategy

### Affiliate Programs
- Amazon Associates (UK & US)
- Spotify Partner Program
- iTunes Affiliate Program
- Steam Partner Program

### Revenue Streams
1. Affiliate commissions from purchases
2. Premium features (advanced search, custom lists)
3. API access for developers
4. Sponsored franchise placements

## Future Enhancements

### Phase 2 Features
1. User accounts and custom lists
2. Community voting on orders
3. Advanced search and filtering
4. Mobile app development
5. Additional API integrations (books, music)

### Technical Improvements
1. Caching layer for API responses
2. Full-text search implementation
3. Image optimization and CDN
4. Performance monitoring
5. SEO optimization

## Security Considerations

### API Security
- Rate limiting on external API calls
- Input validation and sanitization
- CORS configuration
- Environment variable protection

### Data Protection
- No personal data collection initially
- GDPR compliance preparation
- Secure affiliate link generation
- SQL injection prevention

## Testing

### Frontend Testing
- Component unit tests with Jest
- Integration tests for API calls
- Cross-browser compatibility testing
- Mobile responsiveness testing

### Backend Testing
- API endpoint testing
- Database operation testing
- External API integration testing
- Error handling validation

## Maintenance

### Regular Tasks
1. Update franchise data from APIs
2. Monitor affiliate link performance
3. Check for broken external links
4. Update popular franchise rankings
5. Backup database regularly

### Monitoring
- API response times
- Database performance
- User engagement metrics
- Affiliate conversion rates

## Support and Documentation

### User Documentation
- How to find viewing orders
- Understanding different order types
- Using affiliate links
- Mobile app usage

### Developer Documentation
- API reference
- Database schema
- Component documentation
- Deployment guides

---

*This documentation covers the complete OrderOf.org website implementation as of July 2025.*

