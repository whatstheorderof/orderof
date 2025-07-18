from flask import Blueprint, request, jsonify
from src.models.franchise import db, AffiliateLink, Item
import uuid

affiliate_bp = Blueprint('affiliate', __name__)

@affiliate_bp.route('/admin/items/<item_id>/affiliate-links', methods=['POST'])
def create_affiliate_link():
    """Create a new affiliate link for an item"""
    try:
        data = request.get_json()
        item_id = request.view_args['item_id']
        
        if not data or not data.get('platform') or not data.get('url'):
            return jsonify({'error': 'Platform and URL are required'}), 400
        
        # Check if item exists
        item = Item.query.get_or_404(item_id)
        
        affiliate_link = AffiliateLink(
            item_id=item_id,
            platform=data['platform'],
            url=data['url'],
            price=data.get('price'),
            currency=data.get('currency'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(affiliate_link)
        db.session.commit()
        
        return jsonify(affiliate_link.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@affiliate_bp.route('/admin/affiliate-links/<link_id>', methods=['PUT'])
def update_affiliate_link():
    """Update an affiliate link"""
    try:
        data = request.get_json()
        link_id = request.view_args['link_id']
        
        affiliate_link = AffiliateLink.query.get_or_404(link_id)
        
        if data.get('platform'):
            affiliate_link.platform = data['platform']
        if data.get('url'):
            affiliate_link.url = data['url']
        if data.get('price') is not None:
            affiliate_link.price = data['price']
        if data.get('currency'):
            affiliate_link.currency = data['currency']
        if data.get('is_active') is not None:
            affiliate_link.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify(affiliate_link.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@affiliate_bp.route('/admin/affiliate-links/<link_id>', methods=['DELETE'])
def delete_affiliate_link():
    """Delete an affiliate link"""
    try:
        link_id = request.view_args['link_id']
        
        affiliate_link = AffiliateLink.query.get_or_404(link_id)
        
        db.session.delete(affiliate_link)
        db.session.commit()
        
        return jsonify({'message': 'Affiliate link deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@affiliate_bp.route('/affiliate-links/<link_id>/click', methods=['POST'])
def track_affiliate_click():
    """Track affiliate link clicks for analytics"""
    try:
        link_id = request.view_args['link_id']
        data = request.get_json() or {}
        
        affiliate_link = AffiliateLink.query.get_or_404(link_id)
        
        # Here you would typically log the click to an analytics service
        # For now, we'll just return the link URL
        
        click_data = {
            'link_id': link_id,
            'platform': affiliate_link.platform,
            'url': affiliate_link.url,
            'timestamp': data.get('timestamp'),
            'user_agent': request.headers.get('User-Agent'),
            'referrer': request.headers.get('Referer')
        }
        
        # Log click (in a real implementation, you'd save this to a clicks table)
        print(f"Affiliate click tracked: {click_data}")
        
        return jsonify({
            'url': affiliate_link.url,
            'tracked': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@affiliate_bp.route('/admin/affiliate-links/bulk-create', methods=['POST'])
def bulk_create_affiliate_links():
    """Bulk create affiliate links for multiple items"""
    try:
        data = request.get_json()
        
        if not data or not data.get('links'):
            return jsonify({'error': 'Links array is required'}), 400
        
        created_links = []
        
        for link_data in data['links']:
            if not link_data.get('item_id') or not link_data.get('platform') or not link_data.get('url'):
                continue
            
            # Check if item exists
            item = Item.query.get(link_data['item_id'])
            if not item:
                continue
            
            affiliate_link = AffiliateLink(
                item_id=link_data['item_id'],
                platform=link_data['platform'],
                url=link_data['url'],
                price=link_data.get('price'),
                currency=link_data.get('currency'),
                is_active=link_data.get('is_active', True)
            )
            
            db.session.add(affiliate_link)
            created_links.append(affiliate_link)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Created {len(created_links)} affiliate links',
            'links': [link.to_dict() for link in created_links]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@affiliate_bp.route('/admin/affiliate-links/generate-amazon', methods=['POST'])
def generate_amazon_links():
    """Generate Amazon affiliate links for items based on their titles"""
    try:
        data = request.get_json()
        franchise_id = data.get('franchise_id')
        amazon_tag_uk = data.get('amazon_tag_uk', 'orderof-21')  # Replace with actual affiliate tag
        amazon_tag_us = data.get('amazon_tag_us', 'orderof-20')  # Replace with actual affiliate tag
        
        if not franchise_id:
            return jsonify({'error': 'franchise_id is required'}), 400
        
        # Get all items for the franchise
        items = Item.query.filter_by(franchise_id=franchise_id).all()
        
        created_links = []
        
        for item in items:
            # Generate Amazon search URLs (in a real implementation, you'd use Amazon API)
            search_query = item.title.replace(' ', '+')
            
            # Amazon UK link
            amazon_uk_url = f"https://www.amazon.co.uk/s?k={search_query}&tag={amazon_tag_uk}"
            uk_link = AffiliateLink(
                item_id=item.id,
                platform='amazon_uk',
                url=amazon_uk_url,
                currency='GBP',
                is_active=True
            )
            db.session.add(uk_link)
            created_links.append(uk_link)
            
            # Amazon US link
            amazon_us_url = f"https://www.amazon.com/s?k={search_query}&tag={amazon_tag_us}"
            us_link = AffiliateLink(
                item_id=item.id,
                platform='amazon_us',
                url=amazon_us_url,
                currency='USD',
                is_active=True
            )
            db.session.add(us_link)
            created_links.append(us_link)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Generated {len(created_links)} Amazon affiliate links',
            'links_created': len(created_links)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@affiliate_bp.route('/admin/affiliate-stats', methods=['GET'])
def get_affiliate_stats():
    """Get affiliate link statistics"""
    try:
        total_links = AffiliateLink.query.count()
        active_links = AffiliateLink.query.filter_by(is_active=True).count()
        
        # Count by platform
        platform_stats = {}
        platforms = ['amazon_uk', 'amazon_us', 'spotify', 'itunes', 'steam', 'other']
        
        for platform in platforms:
            count = AffiliateLink.query.filter_by(platform=platform, is_active=True).count()
            platform_stats[platform] = count
        
        return jsonify({
            'total_links': total_links,
            'active_links': active_links,
            'inactive_links': total_links - active_links,
            'platform_breakdown': platform_stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

