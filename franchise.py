from flask import Blueprint, request, jsonify
from src.models.franchise import db, Franchise, Item, Order, OrderItem, AffiliateLink
from src.models.user import User
from sqlalchemy import or_, and_
import re

franchise_bp = Blueprint('franchise', __name__)

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-')

@franchise_bp.route('/franchises', methods=['GET'])
def get_franchises():
    """Get all franchises with optional filtering"""
    try:
        category = request.args.get('category')
        search = request.args.get('search')
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        query = Franchise.query
        
        if category:
            query = query.filter(Franchise.category == category)
        
        if search:
            query = query.filter(
                or_(
                    Franchise.name.ilike(f'%{search}%'),
                    Franchise.description.ilike(f'%{search}%')
                )
            )
        
        # Order by popularity score descending
        query = query.order_by(Franchise.popularity_score.desc())
        
        total = query.count()
        franchises = query.offset(offset).limit(limit).all()
        
        return jsonify({
            'franchises': [franchise.to_dict() for franchise in franchises],
            'total': total,
            'limit': limit,
            'offset': offset
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@franchise_bp.route('/franchises/<franchise_id>', methods=['GET'])
def get_franchise(franchise_id):
    """Get a specific franchise by ID"""
    try:
        franchise = Franchise.query.get_or_404(franchise_id)
        return jsonify(franchise.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@franchise_bp.route('/franchises/<franchise_id>/items', methods=['GET'])
def get_franchise_items(franchise_id):
    """Get all items for a specific franchise"""
    try:
        franchise = Franchise.query.get_or_404(franchise_id)
        items = Item.query.filter_by(franchise_id=franchise_id).order_by(Item.release_date).all()
        
        return jsonify({
            'franchise': franchise.to_dict(),
            'items': [item.to_dict() for item in items]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@franchise_bp.route('/franchises/<franchise_id>/orders', methods=['GET'])
def get_franchise_orders(franchise_id):
    """Get all orders for a specific franchise"""
    try:
        franchise = Franchise.query.get_or_404(franchise_id)
        orders = Order.query.filter_by(franchise_id=franchise_id).all()
        
        orders_data = []
        for order in orders:
            order_dict = order.to_dict()
            # Get order items with item details
            order_items = db.session.query(OrderItem, Item).join(Item).filter(
                OrderItem.order_id == order.id
            ).order_by(OrderItem.position).all()
            
            order_dict['items'] = []
            for order_item, item in order_items:
                item_dict = item.to_dict()
                item_dict['position'] = order_item.position
                item_dict['notes'] = order_item.notes
                item_dict['is_optional'] = order_item.is_optional
                
                # Get affiliate links for this item
                affiliate_links = AffiliateLink.query.filter_by(
                    item_id=item.id, is_active=True
                ).all()
                item_dict['affiliate_links'] = [link.to_dict() for link in affiliate_links]
                
                order_dict['items'].append(item_dict)
            
            orders_data.append(order_dict)
        
        return jsonify({
            'franchise': franchise.to_dict(),
            'orders': orders_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@franchise_bp.route('/franchises/<franchise_id>/orders/<order_type>', methods=['GET'])
def get_franchise_order_by_type(franchise_id, order_type):
    """Get a specific order type for a franchise"""
    try:
        franchise = Franchise.query.get_or_404(franchise_id)
        order = Order.query.filter_by(
            franchise_id=franchise_id, 
            order_type=order_type
        ).first()
        
        if not order:
            return jsonify({'error': 'Order type not found'}), 404
        
        order_dict = order.to_dict()
        
        # Get order items with item details
        order_items = db.session.query(OrderItem, Item).join(Item).filter(
            OrderItem.order_id == order.id
        ).order_by(OrderItem.position).all()
        
        order_dict['items'] = []
        for order_item, item in order_items:
            item_dict = item.to_dict()
            item_dict['position'] = order_item.position
            item_dict['notes'] = order_item.notes
            item_dict['is_optional'] = order_item.is_optional
            
            # Get affiliate links for this item
            affiliate_links = AffiliateLink.query.filter_by(
                item_id=item.id, is_active=True
            ).all()
            item_dict['affiliate_links'] = [link.to_dict() for link in affiliate_links]
            
            order_dict['items'].append(item_dict)
        
        return jsonify({
            'franchise': franchise.to_dict(),
            'order': order_dict
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@franchise_bp.route('/categories/<category>/franchises', methods=['GET'])
def get_category_franchises(category):
    """Get franchises by category"""
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        query = Franchise.query.filter_by(category=category)
        query = query.order_by(Franchise.popularity_score.desc())
        
        total = query.count()
        franchises = query.offset(offset).limit(limit).all()
        
        return jsonify({
            'category': category,
            'franchises': [franchise.to_dict() for franchise in franchises],
            'total': total,
            'limit': limit,
            'offset': offset
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@franchise_bp.route('/search', methods=['GET'])
def search():
    """Search across all franchises and items"""
    try:
        query = request.args.get('q', '')
        category = request.args.get('category')
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Search franchises
        franchise_query = Franchise.query.filter(
            or_(
                Franchise.name.ilike(f'%{query}%'),
                Franchise.description.ilike(f'%{query}%')
            )
        )
        
        if category:
            franchise_query = franchise_query.filter(Franchise.category == category)
        
        franchises = franchise_query.order_by(Franchise.popularity_score.desc()).limit(limit).all()
        
        # Search items
        item_query = Item.query.filter(
            or_(
                Item.title.ilike(f'%{query}%'),
                Item.description.ilike(f'%{query}%')
            )
        )
        
        if category:
            item_query = item_query.join(Franchise).filter(Franchise.category == category)
        
        items = item_query.limit(limit).all()
        
        return jsonify({
            'query': query,
            'category': category,
            'franchises': [franchise.to_dict() for franchise in franchises],
            'items': [item.to_dict() for item in items]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@franchise_bp.route('/popular', methods=['GET'])
def get_popular():
    """Get popular franchises"""
    try:
        category = request.args.get('category')
        limit = request.args.get('limit', 10, type=int)
        
        query = Franchise.query
        
        if category:
            query = query.filter(Franchise.category == category)
        
        franchises = query.order_by(Franchise.popularity_score.desc()).limit(limit).all()
        
        return jsonify({
            'category': category,
            'franchises': [franchise.to_dict() for franchise in franchises]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin endpoints for creating/updating data
@franchise_bp.route('/admin/franchises', methods=['POST'])
def create_franchise():
    """Create a new franchise"""
    try:
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('category'):
            return jsonify({'error': 'Name and category are required'}), 400
        
        # Generate slug from name
        slug = slugify(data['name'])
        
        # Check if slug already exists
        existing = Franchise.query.filter_by(slug=slug).first()
        if existing:
            return jsonify({'error': 'Franchise with this name already exists'}), 409
        
        franchise = Franchise(
            name=data['name'],
            slug=slug,
            category=data['category'],
            description=data.get('description'),
            image_url=data.get('image_url'),
            popularity_score=data.get('popularity_score', 0)
        )
        
        db.session.add(franchise)
        db.session.commit()
        
        return jsonify(franchise.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@franchise_bp.route('/admin/franchises/<franchise_id>/items', methods=['POST'])
def create_item():
    """Create a new item for a franchise"""
    try:
        data = request.get_json()
        franchise_id = request.view_args['franchise_id']
        
        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        # Check if franchise exists
        franchise = Franchise.query.get_or_404(franchise_id)
        
        # Generate slug from title
        slug = slugify(data['title'])
        
        item = Item(
            franchise_id=franchise_id,
            title=data['title'],
            slug=slug,
            description=data.get('description'),
            release_date=data.get('release_date'),
            image_url=data.get('image_url'),
            external_id=data.get('external_id'),
            metadata=data.get('metadata')
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify(item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@franchise_bp.route('/admin/franchises/<franchise_id>/orders', methods=['POST'])
def create_order():
    """Create a new order for a franchise"""
    try:
        data = request.get_json()
        franchise_id = request.view_args['franchise_id']
        
        if not data or not data.get('order_type'):
            return jsonify({'error': 'Order type is required'}), 400
        
        # Check if franchise exists
        franchise = Franchise.query.get_or_404(franchise_id)
        
        order = Order(
            franchise_id=franchise_id,
            order_type=data['order_type'],
            name=data.get('name'),
            description=data.get('description'),
            is_official=data.get('is_official', False)
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify(order.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

