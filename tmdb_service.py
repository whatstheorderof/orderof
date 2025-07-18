import requests
import os
from datetime import datetime
from src.models.franchise import db, Franchise, Item, Order, OrderItem

class TMDbService:
    def __init__(self):
        self.api_key = "8b459b6f6aa0f76b7bf3fba33086cb81"
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
    
    def _make_request(self, endpoint, params=None):
        """Make a request to TMDb API"""
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"TMDb API error: {e}")
            return None
    
    def search_movies(self, query):
        """Search for movies by title"""
        return self._make_request("search/movie", {"query": query})
    
    def search_tv_shows(self, query):
        """Search for TV shows by title"""
        return self._make_request("search/tv", {"query": query})
    
    def get_movie_details(self, movie_id):
        """Get detailed information about a movie"""
        return self._make_request(f"movie/{movie_id}")
    
    def get_tv_details(self, tv_id):
        """Get detailed information about a TV show"""
        return self._make_request(f"tv/{tv_id}")
    
    def get_movie_collection(self, collection_id):
        """Get movie collection details"""
        return self._make_request(f"collection/{collection_id}")
    
    def sync_movie_franchise(self, franchise_name, franchise_id):
        """Sync a movie franchise from TMDb"""
        try:
            # Search for the franchise
            search_results = self.search_movies(franchise_name)
            if not search_results or not search_results.get('results'):
                return False
            
            # Look for a movie with a collection
            collection_id = None
            for movie in search_results['results']:
                movie_details = self.get_movie_details(movie['id'])
                if movie_details and movie_details.get('belongs_to_collection'):
                    collection_id = movie_details['belongs_to_collection']['id']
                    break
            
            if not collection_id:
                # If no collection found, just add individual movies
                return self._sync_individual_movies(search_results['results'], franchise_id)
            
            # Get collection details
            collection = self.get_movie_collection(collection_id)
            if not collection:
                return False
            
            # Create items for each movie in the collection
            for movie in collection.get('parts', []):
                self._create_movie_item(movie, franchise_id)
            
            # Create release order
            self._create_movie_release_order(collection.get('parts', []), franchise_id)
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error syncing movie franchise: {e}")
            db.session.rollback()
            return False
    
    def sync_tv_franchise(self, franchise_name, franchise_id):
        """Sync a TV franchise from TMDb"""
        try:
            # Search for the TV show
            search_results = self.search_tv_shows(franchise_name)
            if not search_results or not search_results.get('results'):
                return False
            
            # Get details for the first result (main show)
            main_show = search_results['results'][0]
            tv_details = self.get_tv_details(main_show['id'])
            
            if not tv_details:
                return False
            
            # Create item for the main show
            self._create_tv_item(tv_details, franchise_id)
            
            # Create season-based order if multiple seasons
            if tv_details.get('number_of_seasons', 0) > 1:
                self._create_tv_season_order(tv_details, franchise_id)
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error syncing TV franchise: {e}")
            db.session.rollback()
            return False
    
    def _sync_individual_movies(self, movies, franchise_id):
        """Sync individual movies when no collection is found"""
        try:
            for movie in movies[:5]:  # Limit to first 5 results
                self._create_movie_item(movie, franchise_id)
            
            # Create release order
            self._create_movie_release_order(movies[:5], franchise_id)
            return True
        except Exception as e:
            print(f"Error syncing individual movies: {e}")
            return False
    
    def _create_movie_item(self, movie_data, franchise_id):
        """Create an Item from movie data"""
        try:
            # Check if item already exists
            existing = Item.query.filter_by(
                franchise_id=franchise_id,
                external_id=str(movie_data['id'])
            ).first()
            
            if existing:
                return existing
            
            release_date = None
            if movie_data.get('release_date'):
                try:
                    release_date = datetime.strptime(movie_data['release_date'], '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            image_url = None
            if movie_data.get('poster_path'):
                image_url = f"{self.image_base_url}{movie_data['poster_path']}"
            
            item = Item(
                franchise_id=franchise_id,
                title=movie_data.get('title', ''),
                slug=movie_data.get('title', '').lower().replace(' ', '-'),
                description=movie_data.get('overview', ''),
                release_date=release_date,
                image_url=image_url,
                external_id=str(movie_data['id']),
                api_metadata={
                    'tmdb_id': movie_data['id'],
                    'vote_average': movie_data.get('vote_average'),
                    'vote_count': movie_data.get('vote_count'),
                    'genre_ids': movie_data.get('genre_ids', []),
                    'original_language': movie_data.get('original_language'),
                    'adult': movie_data.get('adult', False)
                }
            )
            
            db.session.add(item)
            return item
            
        except Exception as e:
            print(f"Error creating movie item: {e}")
            return None
    
    def _create_tv_item(self, tv_data, franchise_id):
        """Create an Item from TV show data"""
        try:
            # Check if item already exists
            existing = Item.query.filter_by(
                franchise_id=franchise_id,
                external_id=str(tv_data['id'])
            ).first()
            
            if existing:
                return existing
            
            release_date = None
            if tv_data.get('first_air_date'):
                try:
                    release_date = datetime.strptime(tv_data['first_air_date'], '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            image_url = None
            if tv_data.get('poster_path'):
                image_url = f"{self.image_base_url}{tv_data['poster_path']}"
            
            item = Item(
                franchise_id=franchise_id,
                title=tv_data.get('name', ''),
                slug=tv_data.get('name', '').lower().replace(' ', '-'),
                description=tv_data.get('overview', ''),
                release_date=release_date,
                image_url=image_url,
                external_id=str(tv_data['id']),
                api_metadata={
                    'tmdb_id': tv_data['id'],
                    'vote_average': tv_data.get('vote_average'),
                    'vote_count': tv_data.get('vote_count'),
                    'genre_ids': tv_data.get('genre_ids', []),
                    'original_language': tv_data.get('original_language'),
                    'number_of_seasons': tv_data.get('number_of_seasons'),
                    'number_of_episodes': tv_data.get('number_of_episodes'),
                    'status': tv_data.get('status')
                }
            )
            
            db.session.add(item)
            return item
            
        except Exception as e:
            print(f"Error creating TV item: {e}")
            return None
    
    def _create_movie_release_order(self, movies, franchise_id):
        """Create release order for movies"""
        try:
            # Check if order already exists
            existing_order = Order.query.filter_by(
                franchise_id=franchise_id,
                order_type='release'
            ).first()
            
            if existing_order:
                return existing_order
            
            order = Order(
                franchise_id=franchise_id,
                order_type='release',
                name='Release Order',
                description='Movies in the order they were released',
                is_official=True
            )
            
            db.session.add(order)
            db.session.flush()  # Get the order ID
            
            # Sort movies by release date
            sorted_movies = sorted(movies, key=lambda x: x.get('release_date', ''))
            
            for position, movie in enumerate(sorted_movies, 1):
                item = Item.query.filter_by(
                    franchise_id=franchise_id,
                    external_id=str(movie['id'])
                ).first()
                
                if item:
                    order_item = OrderItem(
                        order_id=order.id,
                        item_id=item.id,
                        position=position
                    )
                    db.session.add(order_item)
            
            return order
            
        except Exception as e:
            print(f"Error creating movie release order: {e}")
            return None
    
    def _create_tv_season_order(self, tv_data, franchise_id):
        """Create season order for TV shows"""
        try:
            # This is a simplified version - in a real implementation,
            # you'd fetch season details and create items for each season
            order = Order(
                franchise_id=franchise_id,
                order_type='chronological',
                name='Season Order',
                description='Episodes/seasons in chronological order',
                is_official=True
            )
            
            db.session.add(order)
            return order
            
        except Exception as e:
            print(f"Error creating TV season order: {e}")
            return None

