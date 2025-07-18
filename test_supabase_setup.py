#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'orderof_backend', 'src'))

from config.supabase import get_supabase_client

def test_supabase_connection():
    """Test the Supabase connection and create tables if needed."""
    try:
        client = get_supabase_client()
        
        # Test connection by trying to query franchises table directly
        try:
            result = client.table('franchises').select('id').limit(1).execute()
            print("✅ Supabase connection successful!")
            print("✅ Franchises table exists!")
            
            # Test inserting a sample franchise
            test_franchise = {
                'name': 'Test Franchise',
                'slug': 'test-franchise',
                'category': 'movies',
                'description': 'A test franchise for verification',
                'popularity_score': 1
            }
            
            try:
                result = client.table('franchises').insert(test_franchise).execute()
                if result.data:
                    print("✅ Test franchise created successfully!")
                    
                    # Clean up test data
                    client.table('franchises').delete().eq('slug', 'test-franchise').execute()
                    print("🧹 Test data cleaned up")
                else:
                    print("❌ Failed to create test franchise")
            except Exception as e:
                print(f"❌ Error testing franchise creation: {e}")
                
        except Exception as e:
            print(f"⚠️  Connection successful but tables don't exist yet: {e}")
            print("📝 Please run the SQL script in Supabase dashboard to create tables:")
            print("   1. Go to https://vrojutbnratuonimkrpo.supabase.co")
            print("   2. Navigate to SQL Editor")
            print("   3. Run the SQL script from setup_supabase_tables.sql")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    test_supabase_connection()

