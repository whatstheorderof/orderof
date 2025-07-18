from flask import Blueprint, request, jsonify
from src.services.supabase_sync_service import SupabaseSyncService
import logging

logger = logging.getLogger(__name__)

supabase_sync_bp = Blueprint('supabase_sync', __name__)
sync_service = SupabaseSyncService()

@supabase_sync_bp.route('/admin/sync/popular', methods=['POST'])
def sync_popular_franchises():
    """Sync popular franchises from various sources."""
    try:
        result = sync_service.sync_popular_franchises()
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Error in sync_popular_franchises: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_sync_bp.route('/admin/sync/tmdb/movies', methods=['POST'])
def sync_tmdb_movies():
    """Sync movies from TMDb for a specific franchise."""
    try:
        data = request.get_json()
        if not data or 'franchise_id' not in data or 'franchise_name' not in data:
            return jsonify({'error': 'Franchise ID and name are required'}), 400
        
        result = sync_service.sync_tmdb_movies_for_franchise(
            data['franchise_id'], 
            data['franchise_name']
        )
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Error in sync_tmdb_movies: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_sync_bp.route('/admin/sync/rawg/games', methods=['POST'])
def sync_rawg_games():
    """Sync games from RAWG for a specific franchise."""
    try:
        data = request.get_json()
        if not data or 'franchise_id' not in data or 'franchise_name' not in data:
            return jsonify({'error': 'Franchise ID and name are required'}), 400
        
        result = sync_service.sync_rawg_games_for_franchise(
            data['franchise_id'], 
            data['franchise_name']
        )
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Error in sync_rawg_games: {e}")
        return jsonify({'error': 'Internal server error'}), 500

