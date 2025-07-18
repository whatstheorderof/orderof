import requests
from datetime import datetime
from src.models.franchise import db, Franchise, Item, Order, OrderItem

class RAWGService:
    def __init__(self):
        self.api_key = "e27f4f6149ec4c358472cfd6913e6d85"
        self.base_url = "https://api.rawg.io/api"
    
    def _make_request(self, endpoint, params=None):
        """Make a request to RAWG API"""
        if params is None:
            params = {}
        params['key'] = self.api_key
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"RAWG API error: {e}")
            return None
    
    def search_games(self, query):
        """Search for games by title"""
        return self._make_request("games", {"search": query})
    
    def get_game_details(self, game_id):
        """Get detailed information about a game"""
        return self._make_request(f"games/{game_id}")
    
    def get_game_series(self, series_name):
        """Get games in a series"""
        # RAWG doesn't have a direct series endpoint, so we search and filter
        search_results = self.search_games(series_name)
        if not search_results:
            return None
        
        # Filter results to find games that likely belong to the series
        series_games = []
        for game in search_results.get('results', []):
            if series_name.lower() in game.get('name', '').lower():
                series_games.append(game)
        
        return {'results': series_games}
    
    def sync_game_franchise(self, franchise_name, franchise_id):
        """Sync a game franchise from RAWG"""
        try:
            # Search for games in the franchise
            search_results = self.get_game_series(franchise_name)
            if not search_results or not search_results.get('results'):
                # Fallback to regular search
                search_results = self.search_games(franchise_name)
            
            if not search_results or not search_results.get('results'):
                return False
            
            games = search_results['results'][:10]  # Limit to first 10 results
            
            # Create items for each game
            for game in games:
                self._create_game_item(game, franchise_id)
            
            # Create release order
            self._create_game_release_order(games, franchise_id)
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error syncing game franchise: {e}")
            db.session.rollback()
            return False
    
    def _create_game_item(self, game_data, franchise_id):
        """Create an Item from game data"""
        try:
            # Check if item already exists
            existing = Item.query.filter_by(
                franchise_id=franchise_id,
                external_id=str(game_data['id'])
            ).first()
            
            if existing:
                return existing
            
            release_date = None
            if game_data.get('released'):
                try:
                    release_date = datetime.strptime(game_data['released'], '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            # Get platforms
            platforms = []
            if game_data.get('platforms'):
                platforms = [p['platform']['name'] for p in game_data['platforms']]
            
            # Get genres
            genres = []
            if game_data.get('genres'):
                genres = [g['name'] for g in game_data['genres']]
            
            item = Item(
                franchise_id=franchise_id,
                title=game_data.get('name', ''),
                slug=game_data.get('slug', ''),
                description=game_data.get('description_raw', ''),
                release_date=release_date,
                image_url=game_data.get('background_image'),
                external_id=str(game_data['id']),
                api_metadata={
                    'rawg_id': game_data['id'],
                    'rating': game_data.get('rating'),
                    'rating_top': game_data.get('rating_top'),
                    'ratings_count': game_data.get('ratings_count'),
                    'metacritic': game_data.get('metacritic'),
                    'platforms': platforms,
                    'genres': genres,
                    'developers': [d['name'] for d in game_data.get('developers', [])],
                    'publishers': [p['name'] for p in game_data.get('publishers', [])],
                    'esrb_rating': game_data.get('esrb_rating', {}).get('name') if game_data.get('esrb_rating') else None
                }
            )
            
            db.session.add(item)
            return item
            
        except Exception as e:
            print(f"Error creating game item: {e}")
            return None
    
    def _create_game_release_order(self, games, franchise_id):
        """Create release order for games"""
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
                description='Games in the order they were released',
                is_official=True
            )
            
            db.session.add(order)
            db.session.flush()  # Get the order ID
            
            # Sort games by release date
            sorted_games = sorted(games, key=lambda x: x.get('released', ''))
            
            for position, game in enumerate(sorted_games, 1):
                item = Item.query.filter_by(
                    franchise_id=franchise_id,
                    external_id=str(game['id'])
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
            print(f"Error creating game release order: {e}")
            return None
    
    def get_popular_games(self, limit=20):
        """Get popular games"""
        return self._make_request("games", {
            "ordering": "-rating",
            "page_size": limit
        })
    
    def get_games_by_genre(self, genre_id, limit=20):
        """Get games by genre"""
        return self._make_request("games", {
            "genres": genre_id,
            "page_size": limit
        })
    
    def get_games_by_platform(self, platform_id, limit=20):
        """Get games by platform"""
        return self._make_request("games", {
            "platforms": platform_id,
            "page_size": limit
        })

