from typing import List, Dict, Any
import requests
from datetime import datetime
from src.services.supabase_service import SupabaseService
from src.services.tmdb_service import TMDbService
from src.services.rawg_service import RAWGService
import logging

logger = logging.getLogger(__name__)

class SupabaseSyncService:
    def __init__(self):
        self.supabase_service = SupabaseService()
        self.tmdb_service = TMDbService()
        self.rawg_service = RAWGService()
    
    def sync_popular_franchises(self) -> Dict[str, Any]:
        """Sync popular franchises from various APIs."""
        try:
            created_franchises = []
            
            # Popular movie franchises
            movie_franchises = [
                "Star Wars", "Marvel Cinematic Universe", "Harry Potter", 
                "The Lord of the Rings", "Fast & Furious", "James Bond",
                "Mission: Impossible", "Jurassic Park", "Transformers", "X-Men"
            ]
            
            for franchise_name in movie_franchises:
                franchise_data = {
                    'name': franchise_name,
                    'slug': franchise_name.lower().replace(' ', '-').replace('&', 'and'),
                    'category': 'movies',
                    'description': f'Popular movie franchise: {franchise_name}',
                    'popularity_score': 100
                }
                
                franchise = self.supabase_service.create_franchise(franchise_data)
                if franchise:
                    created_franchises.append(franchise)
                    
                    # Sync movies for this franchise
                    self.sync_tmdb_movies_for_franchise(franchise['id'], franchise_name)
            
            # Popular TV series
            tv_franchises = [
                "Game of Thrones", "Breaking Bad", "The Walking Dead",
                "Stranger Things", "The Office", "Friends", "Marvel",
                "Star Trek", "Doctor Who", "Sherlock"
            ]
            
            for franchise_name in tv_franchises:
                franchise_data = {
                    'name': franchise_name,
                    'slug': franchise_name.lower().replace(' ', '-').replace('&', 'and'),
                    'category': 'series',
                    'description': f'Popular TV franchise: {franchise_name}',
                    'popularity_score': 100
                }
                
                franchise = self.supabase_service.create_franchise(franchise_data)
                if franchise:
                    created_franchises.append(franchise)
            
            # Popular game franchises
            game_franchises = [
                "The Legend of Zelda", "Super Mario", "Call of Duty",
                "Grand Theft Auto", "The Elder Scrolls", "Final Fantasy",
                "Assassin's Creed", "Halo", "Pokemon", "The Witcher"
            ]
            
            for franchise_name in game_franchises:
                franchise_data = {
                    'name': franchise_name,
                    'slug': franchise_name.lower().replace(' ', '-').replace('&', 'and'),
                    'category': 'games',
                    'description': f'Popular game franchise: {franchise_name}',
                    'popularity_score': 100
                }
                
                franchise = self.supabase_service.create_franchise(franchise_data)
                if franchise:
                    created_franchises.append(franchise)
            
            return {
                'message': f'Synced {len(created_franchises)} popular franchises',
                'franchises': created_franchises
            }
        except Exception as e:
            logger.error(f"Error syncing popular franchises: {e}")
            return {'error': str(e)}
    
    def sync_tmdb_movies_for_franchise(self, franchise_id: str, franchise_name: str) -> Dict[str, Any]:
        """Sync movies from TMDb for a specific franchise."""
        try:
            # Search for movies related to the franchise
            search_url = f"https://api.themoviedb.org/3/search/movie"
            params = {
                'api_key': self.tmdb_service.api_key,
                'query': franchise_name,
                'language': 'en-US'
            }
            
            response = requests.get(search_url, params=params)
            if response.status_code != 200:
                return {'error': 'Failed to fetch from TMDb'}
            
            data = response.json()
            created_items = []
            
            # Create items for each movie
            for i, movie in enumerate(data.get('results', [])[:10]):  # Limit to 10 movies
                item_data = {
                    'franchise_id': franchise_id,
                    'title': movie.get('title', ''),
                    'description': movie.get('overview', ''),
                    'release_date': movie.get('release_date'),
                    'image_url': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None,
                    'external_id': str(movie.get('id')),
                    'api_metadata': {
                        'tmdb_id': movie.get('id'),
                        'vote_average': movie.get('vote_average'),
                        'vote_count': movie.get('vote_count'),
                        'popularity': movie.get('popularity')
                    },
                    'rating': movie.get('vote_average')
                }
                
                item = self.supabase_service.create_item(item_data)
                if item:
                    created_items.append(item)
            
            # Create a release order for the franchise
            if created_items:
                order_data = {
                    'franchise_id': franchise_id,
                    'name': 'Release Order',
                    'order_type': 'release',
                    'description': 'Movies in the order they were released'
                }
                
                order = self.supabase_service.create_order(order_data)
                if order:
                    # Add items to the order
                    for i, item in enumerate(sorted(created_items, key=lambda x: x.get('release_date', ''))):
                        self.supabase_service.add_item_to_order(order['id'], item['id'], i + 1)
            
            return {
                'message': f'Synced {len(created_items)} movies for {franchise_name}',
                'items': created_items
            }
        except Exception as e:
            logger.error(f"Error syncing TMDb movies for {franchise_name}: {e}")
            return {'error': str(e)}
    
    def sync_rawg_games_for_franchise(self, franchise_id: str, franchise_name: str) -> Dict[str, Any]:
        """Sync games from RAWG for a specific franchise."""
        try:
            # Search for games related to the franchise
            search_url = "https://api.rawg.io/api/games"
            params = {
                'key': self.rawg_service.api_key,
                'search': franchise_name,
                'page_size': 10
            }
            
            response = requests.get(search_url, params=params)
            if response.status_code != 200:
                return {'error': 'Failed to fetch from RAWG'}
            
            data = response.json()
            created_items = []
            
            # Create items for each game
            for game in data.get('results', []):
                item_data = {
                    'franchise_id': franchise_id,
                    'title': game.get('name', ''),
                    'description': game.get('description_raw', ''),
                    'release_date': game.get('released'),
                    'image_url': game.get('background_image'),
                    'external_id': str(game.get('id')),
                    'api_metadata': {
                        'rawg_id': game.get('id'),
                        'rating': game.get('rating'),
                        'ratings_count': game.get('ratings_count'),
                        'metacritic': game.get('metacritic'),
                        'platforms': [p.get('platform', {}).get('name') for p in game.get('platforms', [])]
                    },
                    'rating': game.get('rating')
                }
                
                item = self.supabase_service.create_item(item_data)
                if item:
                    created_items.append(item)
            
            return {
                'message': f'Synced {len(created_items)} games for {franchise_name}',
                'items': created_items
            }
        except Exception as e:
            logger.error(f"Error syncing RAWG games for {franchise_name}: {e}")
            return {'error': str(e)}

