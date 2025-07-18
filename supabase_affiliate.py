from flask import Blueprint, request, jsonify
from src.services.supabase_service import SupabaseService
import logging

logger = logging.getLogger(__name__)

supabase_affiliate_bp = Blueprint('supabase_affiliate', __name__)
supabase_service = SupabaseService()

@supabase_affiliate_bp.route('/items/<item_id>/affiliate-links', methods=['GET'])
def get_item_affiliate_links(item_id):
    """Get all affiliate links for an item."""
    try:
        links = supabase_service.get_item_affiliate_links(item_id)
        return jsonify({'affiliate_links': links}), 200
    except Exception as e:
        logger.error(f"Error in get_item_affiliate_links: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_affiliate_bp.route('/admin/items/<item_id>/affiliate-links', methods=['POST'])
def create_affiliate_link(item_id):
    """Create a new affiliate link for an item."""
    try:
        data = request.get_json()
        if not data or 'platform' not in data or 'region' not in data or 'url' not in data:
            return jsonify({'error': 'Platform, region, and URL are required'}), 400
        
        # Add item_id to the data
        data['item_id'] = item_id
        
        # Set default affiliate tags if not provided
        if 'affiliate_tag' not in data:
            if data['platform'].lower() == 'amazon':
                if data['region'].lower() == 'uk':
                    data['affiliate_tag'] = 'orderof-21'
                elif data['region'].lower() == 'us':
                    data['affiliate_tag'] = 'orderof-20'
        
        link = supabase_service.create_affiliate_link(data)
        if not link:
            return jsonify({'error': 'Failed to create affiliate link'}), 500
        
        return jsonify(link), 201
    except Exception as e:
        logger.error(f"Error in create_affiliate_link: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_affiliate_bp.route('/admin/affiliate-links/<link_id>', methods=['PUT'])
def update_affiliate_link(link_id):
    """Update an existing affiliate link."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        link = supabase_service.update_affiliate_link(link_id, data)
        if not link:
            return jsonify({'error': 'Failed to update affiliate link'}), 500
        
        return jsonify(link), 200
    except Exception as e:
        logger.error(f"Error in update_affiliate_link: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_affiliate_bp.route('/admin/affiliate-links/<link_id>', methods=['DELETE'])
def delete_affiliate_link(link_id):
    """Delete an affiliate link."""
    try:
        success = supabase_service.delete_affiliate_link(link_id)
        if not success:
            return jsonify({'error': 'Failed to delete affiliate link'}), 500
        
        return jsonify({'message': 'Affiliate link deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Error in delete_affiliate_link: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@supabase_affiliate_bp.route('/admin/affiliate-links/generate-amazon', methods=['POST'])
def generate_amazon_affiliate_links():
    """Generate Amazon affiliate links for a franchise."""
    try:
        data = request.get_json()
        if not data or 'franchise_id' not in data:
            return jsonify({'error': 'Franchise ID is required'}), 400
        
        franchise_id = data['franchise_id']
        
        # Get all items for the franchise
        items = supabase_service.get_franchise_items(franchise_id)
        
        created_links = []
        for item in items:
            # Generate Amazon UK link
            uk_link_data = {
                'item_id': item['id'],
                'platform': 'amazon',
                'region': 'uk',
                'url': f"https://www.amazon.co.uk/s?k={item['title'].replace(' ', '+')}&tag=orderof-21",
                'affiliate_tag': 'orderof-21',
                'currency': 'GBP'
            }
            
            # Generate Amazon US link
            us_link_data = {
                'item_id': item['id'],
                'platform': 'amazon',
                'region': 'us',
                'url': f"https://www.amazon.com/s?k={item['title'].replace(' ', '+')}&tag=orderof-20",
                'affiliate_tag': 'orderof-20',
                'currency': 'USD'
            }
            
            # Create the links
            uk_link = supabase_service.create_affiliate_link(uk_link_data)
            us_link = supabase_service.create_affiliate_link(us_link_data)
            
            if uk_link:
                created_links.append(uk_link)
            if us_link:
                created_links.append(us_link)
        
        return jsonify({
            'message': f'Generated {len(created_links)} affiliate links',
            'links': created_links
        }), 201
    except Exception as e:
        logger.error(f"Error in generate_amazon_affiliate_links: {e}")
        return jsonify({'error': 'Internal server error'}), 500

