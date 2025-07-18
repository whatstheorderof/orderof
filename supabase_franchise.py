from flask import Blueprint, request, jsonify
from src.services.supabase_service import SupabaseService
import logging

logger = logging.getLogger(__name__)

supabase_franchise_bp = Blueprint('supabase_franchise', __name__)
supabase_service = SupabaseService()

@supabase_franchise_bp.route('/franchises', methods=['GET'])
def get_franchises():
    """Get all franchises with optional filtering."""
    try:
        category = request.args.get('category')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        result = supabase_service.get_franchises(category=category, limit=limit, offset=offset)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in get_franchises: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_franchise_bp.route('/franchises/<franchise_id>', methods=['GET'])
def get_franchise(franchise_id):
    """Get a specific franchise by ID."""
    try:
        franchise = supabase_service.get_franchise_by_id(franchise_id)
        if not franchise:
            return jsonify({'error': 'Franchise not found'}), 404
        
        return jsonify(franchise), 200
    except Exception as e:
        logger.error(f"Error in get_franchise: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_franchise_bp.route('/franchises/<franchise_id>/items', methods=['GET'])
def get_franchise_items(franchise_id):
    """Get all items for a franchise."""
    try:
        items = supabase_service.get_franchise_items(franchise_id)
        return jsonify({'items': items}), 200
    except Exception as e:
        logger.error(f"Error in get_franchise_items: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_franchise_bp.route('/franchises/<franchise_id>/orders', methods=['GET'])
def get_franchise_orders(franchise_id):
    """Get all orders for a franchise."""
    try:
        result = supabase_service.get_franchise_orders(franchise_id)
        if not result['franchise']:
            return jsonify({'error': 'Franchise not found'}), 404
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in get_franchise_orders: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_franchise_bp.route('/search', methods=['GET'])
def search_franchises():
    """Search franchises by name or description."""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'franchises': []}), 200
        
        limit = int(request.args.get('limit', 20))
        franchises = supabase_service.search_franchises(query, limit)
        
        return jsonify({'franchises': franchises}), 200
    except Exception as e:
        logger.error(f"Error in search_franchises: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Admin routes for creating/updating data
@supabase_franchise_bp.route('/admin/franchises', methods=['POST'])
def create_franchise():
    """Create a new franchise."""
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'category' not in data:
            return jsonify({'error': 'Name and category are required'}), 400
        
        franchise = supabase_service.create_franchise(data)
        if not franchise:
            return jsonify({'error': 'Failed to create franchise'}), 500
        
        return jsonify(franchise), 201
    except Exception as e:
        logger.error(f"Error in create_franchise: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_franchise_bp.route('/admin/franchises/<franchise_id>', methods=['PUT'])
def update_franchise(franchise_id):
    """Update an existing franchise."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        franchise = supabase_service.update_franchise(franchise_id, data)
        if not franchise:
            return jsonify({'error': 'Failed to update franchise'}), 500
        
        return jsonify(franchise), 200
    except Exception as e:
        logger.error(f"Error in update_franchise: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_franchise_bp.route('/admin/items', methods=['POST'])
def create_item():
    """Create a new item."""
    try:
        data = request.get_json()
        if not data or 'franchise_id' not in data or 'title' not in data:
            return jsonify({'error': 'Franchise ID and title are required'}), 400
        
        item = supabase_service.create_item(data)
        if not item:
            return jsonify({'error': 'Failed to create item'}), 500
        
        return jsonify(item), 201
    except Exception as e:
        logger.error(f"Error in create_item: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_franchise_bp.route('/admin/orders', methods=['POST'])
def create_order():
    """Create a new order."""
    try:
        data = request.get_json()
        if not data or 'franchise_id' not in data or 'name' not in data or 'order_type' not in data:
            return jsonify({'error': 'Franchise ID, name, and order type are required'}), 400
        
        order = supabase_service.create_order(data)
        if not order:
            return jsonify({'error': 'Failed to create order'}), 500
        
        return jsonify(order), 201
    except Exception as e:
        logger.error(f"Error in create_order: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_franchise_bp.route('/admin/orders/<order_id>/items', methods=['POST'])
def add_item_to_order(order_id):
    """Add an item to an order."""
    try:
        data = request.get_json()
        if not data or 'item_id' not in data or 'position' not in data:
            return jsonify({'error': 'Item ID and position are required'}), 400
        
        order_item = supabase_service.add_item_to_order(
            order_id, 
            data['item_id'], 
            data['position'], 
            data.get('notes')
        )
        if not order_item:
            return jsonify({'error': 'Failed to add item to order'}), 500
        
        return jsonify(order_item), 201
    except Exception as e:
        logger.error(f"Error in add_item_to_order: {e}")
        return jsonify({'error': 'Internal server error'}), 500

