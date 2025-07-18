from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from src.config.supabase import get_supabase_client
import logging

logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self):
        self.client = get_supabase_client()
    
    # Franchise operations
    def get_franchises(self, category: Optional[str] = None, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Get franchises with optional filtering."""
        try:
            query = self.client.table('franchises').select('*')
            
            if category:
                query = query.eq('category', category)
            
            query = query.order('popularity_score', desc=True).range(offset, offset + limit - 1)
            
            result = query.execute()
            return {
                'franchises': result.data,
                'total': len(result.data)
            }
        except Exception as e:
            logger.error(f"Error fetching franchises: {e}")
            return {'franchises': [], 'total': 0}
    
    def get_franchise_by_id(self, franchise_id: str) -> Optional[Dict[str, Any]]:
        """Get a single franchise by ID."""
        try:
            result = self.client.table('franchises').select('*').eq('id', franchise_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error fetching franchise {franchise_id}: {e}")
            return None
    
    def create_franchise(self, franchise_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new franchise."""
        try:
            # Generate slug if not provided
            if 'slug' not in franchise_data:
                franchise_data['slug'] = franchise_data['name'].lower().replace(' ', '-').replace('&', 'and')
            
            result = self.client.table('franchises').insert(franchise_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error creating franchise: {e}")
            return None
    
    def update_franchise(self, franchise_id: str, franchise_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing franchise."""
        try:
            franchise_data['updated_at'] = datetime.utcnow().isoformat()
            result = self.client.table('franchises').update(franchise_data).eq('id', franchise_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error updating franchise {franchise_id}: {e}")
            return None
    
    # Item operations
    def get_franchise_items(self, franchise_id: str) -> List[Dict[str, Any]]:
        """Get all items for a franchise."""
        try:
            result = self.client.table('items').select('*').eq('franchise_id', franchise_id).order('release_date').execute()
            return result.data
        except Exception as e:
            logger.error(f"Error fetching items for franchise {franchise_id}: {e}")
            return []
    
    def create_item(self, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new item."""
        try:
            result = self.client.table('items').insert(item_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error creating item: {e}")
            return None
    
    def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a single item by ID."""
        try:
            result = self.client.table('items').select('*').eq('id', item_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error fetching item {item_id}: {e}")
            return None
    
    # Order operations
    def get_franchise_orders(self, franchise_id: str) -> Dict[str, Any]:
        """Get all orders for a franchise with their items."""
        try:
            # Get franchise info
            franchise = self.get_franchise_by_id(franchise_id)
            if not franchise:
                return {'franchise': None, 'orders': []}
            
            # Get orders
            orders_result = self.client.table('orders').select('*').eq('franchise_id', franchise_id).execute()
            orders = orders_result.data
            
            # Get order items for each order
            for order in orders:
                order_items_result = self.client.table('order_items').select('''
                    *,
                    items (*)
                ''').eq('order_id', order['id']).order('position').execute()
                
                order['items'] = []
                for order_item in order_items_result.data:
                    item = order_item['items']
                    item['position'] = order_item['position']
                    item['notes'] = order_item['notes']
                    order['items'].append(item)
            
            return {
                'franchise': franchise,
                'orders': orders
            }
        except Exception as e:
            logger.error(f"Error fetching orders for franchise {franchise_id}: {e}")
            return {'franchise': None, 'orders': []}
    
    def create_order(self, order_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new order."""
        try:
            result = self.client.table('orders').insert(order_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return None
    
    def add_item_to_order(self, order_id: str, item_id: str, position: int, notes: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Add an item to an order."""
        try:
            order_item_data = {
                'order_id': order_id,
                'item_id': item_id,
                'position': position,
                'notes': notes
            }
            result = self.client.table('order_items').insert(order_item_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error adding item to order: {e}")
            return None
    
    # Affiliate link operations
    def get_item_affiliate_links(self, item_id: str) -> List[Dict[str, Any]]:
        """Get all affiliate links for an item."""
        try:
            result = self.client.table('affiliate_links').select('*').eq('item_id', item_id).execute()
            return result.data
        except Exception as e:
            logger.error(f"Error fetching affiliate links for item {item_id}: {e}")
            return []
    
    def create_affiliate_link(self, link_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new affiliate link."""
        try:
            result = self.client.table('affiliate_links').insert(link_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error creating affiliate link: {e}")
            return None
    
    def update_affiliate_link(self, link_id: str, link_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing affiliate link."""
        try:
            link_data['updated_at'] = datetime.utcnow().isoformat()
            result = self.client.table('affiliate_links').update(link_data).eq('id', link_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error updating affiliate link {link_id}: {e}")
            return None
    
    def delete_affiliate_link(self, link_id: str) -> bool:
        """Delete an affiliate link."""
        try:
            result = self.client.table('affiliate_links').delete().eq('id', link_id).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Error deleting affiliate link {link_id}: {e}")
            return False
    
    # Search operations
    def search_franchises(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search franchises by name or description."""
        try:
            # Use ilike for case-insensitive search
            result = self.client.table('franchises').select('*').or_(
                f'name.ilike.%{query}%,description.ilike.%{query}%'
            ).order('popularity_score', desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            logger.error(f"Error searching franchises: {e}")
            return []

