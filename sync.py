from flask import Blueprint, request, jsonify
from src.models.franchise import db, Franchise
from src.services.tmdb_service import TMDbService
from src.services.rawg_service import RAWGService
import re

sync_bp = Blueprint('sync', __name__)

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-')

@sync_bp.route('/admin/sync/tmdb/movies', methods=['POST'])
def sync_tmdb_movies():
    """Sync movie franchise from TMDb"""
    try:
        data = request.get_json()
        franchise_name = data.get('franchise_name')
        
        if not franchise_name:
            return jsonify({'error': 'franchise_name is required'}), 400
        
        # Check if franchise exists, create if not
        slug = slugify(franchise_name)
        franchise = Franchise.query.filter_by(slug=slug).first()
        
        if not franchise:
            franchise = Franchise(
                name=franchise_name,
                slug=slug,
                category='movies',
                description=f'Movie franchise: {franchise_name}',
                popularity_score=50
            )
            db.session.add(franchise)
            db.session.commit()
        
        # Sync with TMDb
        tmdb_service = TMDbService()
        success = tmdb_service.sync_movie_franchise(franchise_name, franchise.id)
        
        if success:
            return jsonify({
                'message': f'Successfully synced {franchise_name} from TMDb',
                'franchise': franchise.to_dict()
            })
        else:
            return jsonify({'error': 'Failed to sync franchise from TMDb'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sync_bp.route('/admin/sync/tmdb/tv', methods=['POST'])
def sync_tmdb_tv():
    """Sync TV franchise from TMDb"""
    try:
        data = request.get_json()
        franchise_name = data.get('franchise_name')
        
        if not franchise_name:
            return jsonify({'error': 'franchise_name is required'}), 400
        
        # Check if franchise exists, create if not
        slug = slugify(franchise_name)
        franchise = Franchise.query.filter_by(slug=slug).first()
        
        if not franchise:
            franchise = Franchise(
                name=franchise_name,
                slug=slug,
                category='series',
                description=f'TV series franchise: {franchise_name}',
                popularity_score=50
            )
            db.session.add(franchise)
            db.session.commit()
        
        # Sync with TMDb
        tmdb_service = TMDbService()
        success = tmdb_service.sync_tv_franchise(franchise_name, franchise.id)
        
        if success:
            return jsonify({
                'message': f'Successfully synced {franchise_name} from TMDb',
                'franchise': franchise.to_dict()
            })
        else:
            return jsonify({'error': 'Failed to sync franchise from TMDb'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sync_bp.route('/admin/sync/rawg/games', methods=['POST'])
def sync_rawg_games():
    """Sync game franchise from RAWG"""
    try:
        data = request.get_json()
        franchise_name = data.get('franchise_name')
        
        if not franchise_name:
            return jsonify({'error': 'franchise_name is required'}), 400
        
        # Check if franchise exists, create if not
        slug = slugify(franchise_name)
        franchise = Franchise.query.filter_by(slug=slug).first()
        
        if not franchise:
            franchise = Franchise(
                name=franchise_name,
                slug=slug,
                category='games',
                description=f'Game franchise: {franchise_name}',
                popularity_score=50
            )
            db.session.add(franchise)
            db.session.commit()
        
        # Sync with RAWG
        rawg_service = RAWGService()
        success = rawg_service.sync_game_franchise(franchise_name, franchise.id)
        
        if success:
            return jsonify({
                'message': f'Successfully synced {franchise_name} from RAWG',
                'franchise': franchise.to_dict()
            })
        else:
            return jsonify({'error': 'Failed to sync franchise from RAWG'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sync_bp.route('/admin/sync/popular', methods=['POST'])
def sync_popular_franchises():
    """Sync popular franchises from multiple APIs"""
    try:
        # Popular movie franchises
        movie_franchises = [
            'Marvel Cinematic Universe',
            'Star Wars',
            'Harry Potter',
            'The Lord of the Rings',
            'Fast & Furious',
            'James Bond',
            'Mission: Impossible',
            'Jurassic Park',
            'Transformers',
            'X-Men'
        ]
        
        # Popular game franchises
        game_franchises = [
            'The Legend of Zelda',
            'Super Mario',
            'Call of Duty',
            'Grand Theft Auto',
            'The Elder Scrolls',
            'Final Fantasy',
            'Assassin\'s Creed',
            'Halo',
            'Pokemon',
            'The Witcher'
        ]
        
        # Popular TV franchises
        tv_franchises = [
            'Game of Thrones',
            'Breaking Bad',
            'The Walking Dead',
            'Stranger Things',
            'The Office',
            'Friends',
            'Marvel',
            'Star Trek',
            'Doctor Who',
            'Sherlock'
        ]
        
        tmdb_service = TMDbService()
        rawg_service = RAWGService()
        
        synced_count = 0
        
        # Sync movie franchises
        for franchise_name in movie_franchises:
            try:
                slug = slugify(franchise_name)
                existing = Franchise.query.filter_by(slug=slug).first()
                
                if not existing:
                    franchise = Franchise(
                        name=franchise_name,
                        slug=slug,
                        category='movies',
                        description=f'Popular movie franchise: {franchise_name}',
                        popularity_score=100
                    )
                    db.session.add(franchise)
                    db.session.commit()
                    
                    if tmdb_service.sync_movie_franchise(franchise_name, franchise.id):
                        synced_count += 1
            except Exception as e:
                print(f"Error syncing {franchise_name}: {e}")
                continue
        
        # Sync game franchises
        for franchise_name in game_franchises:
            try:
                slug = slugify(franchise_name)
                existing = Franchise.query.filter_by(slug=slug).first()
                
                if not existing:
                    franchise = Franchise(
                        name=franchise_name,
                        slug=slug,
                        category='games',
                        description=f'Popular game franchise: {franchise_name}',
                        popularity_score=100
                    )
                    db.session.add(franchise)
                    db.session.commit()
                    
                    if rawg_service.sync_game_franchise(franchise_name, franchise.id):
                        synced_count += 1
            except Exception as e:
                print(f"Error syncing {franchise_name}: {e}")
                continue
        
        # Sync TV franchises
        for franchise_name in tv_franchises:
            try:
                slug = slugify(franchise_name)
                existing = Franchise.query.filter_by(slug=slug).first()
                
                if not existing:
                    franchise = Franchise(
                        name=franchise_name,
                        slug=slug,
                        category='series',
                        description=f'Popular TV franchise: {franchise_name}',
                        popularity_score=100
                    )
                    db.session.add(franchise)
                    db.session.commit()
                    
                    if tmdb_service.sync_tv_franchise(franchise_name, franchise.id):
                        synced_count += 1
            except Exception as e:
                print(f"Error syncing {franchise_name}: {e}")
                continue
        
        return jsonify({
            'message': f'Successfully synced {synced_count} popular franchises',
            'total_attempted': len(movie_franchises) + len(game_franchises) + len(tv_franchises)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sync_bp.route('/admin/sync/status', methods=['GET'])
def get_sync_status():
    """Get sync status and statistics"""
    try:
        total_franchises = Franchise.query.count()
        
        stats = {
            'total_franchises': total_franchises,
            'by_category': {}
        }
        
        categories = ['movies', 'series', 'games', 'books', 'music', 'cars', 'anime']
        for category in categories:
            count = Franchise.query.filter_by(category=category).count()
            stats['by_category'][category] = count
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

