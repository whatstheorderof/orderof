-- OrderOf.org Supabase Database Schema

-- Create franchises table
CREATE TABLE IF NOT EXISTS franchises (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    image_url TEXT,
    external_id VARCHAR(100),
    api_metadata JSONB,
    popularity_score INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create items table
CREATE TABLE IF NOT EXISTS items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    franchise_id UUID REFERENCES franchises(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    release_date DATE,
    image_url TEXT,
    external_id VARCHAR(100),
    api_metadata JSONB,
    rating DECIMAL(3,1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    franchise_id UUID REFERENCES franchises(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    order_type VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    item_id UUID REFERENCES items(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(order_id, position)
);

-- Create affiliate_links table
CREATE TABLE IF NOT EXISTS affiliate_links (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    item_id UUID REFERENCES items(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    region VARCHAR(10) NOT NULL,
    url TEXT NOT NULL,
    price DECIMAL(10,2),
    currency VARCHAR(3),
    affiliate_tag VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(item_id, platform, region)
);

-- Enable Row Level Security
ALTER TABLE franchises ENABLE ROW LEVEL SECURITY;
ALTER TABLE items ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE affiliate_links ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access
CREATE POLICY IF NOT EXISTS "Public read access" ON franchises FOR SELECT USING (true);
CREATE POLICY IF NOT EXISTS "Public read access" ON items FOR SELECT USING (true);
CREATE POLICY IF NOT EXISTS "Public read access" ON orders FOR SELECT USING (true);
CREATE POLICY IF NOT EXISTS "Public read access" ON order_items FOR SELECT USING (true);
CREATE POLICY IF NOT EXISTS "Public read access" ON affiliate_links FOR SELECT USING (true);

-- Create policies for service role (for backend operations)
CREATE POLICY IF NOT EXISTS "Service role full access" ON franchises FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY IF NOT EXISTS "Service role full access" ON items FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY IF NOT EXISTS "Service role full access" ON orders FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY IF NOT EXISTS "Service role full access" ON order_items FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY IF NOT EXISTS "Service role full access" ON affiliate_links FOR ALL USING (auth.role() = 'service_role');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_franchises_category ON franchises(category);
CREATE INDEX IF NOT EXISTS idx_franchises_popularity ON franchises(popularity_score DESC);
CREATE INDEX IF NOT EXISTS idx_items_franchise_id ON items(franchise_id);
CREATE INDEX IF NOT EXISTS idx_items_release_date ON items(release_date);
CREATE INDEX IF NOT EXISTS idx_orders_franchise_id ON orders(franchise_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_position ON order_items(order_id, position);
CREATE INDEX IF NOT EXISTS idx_affiliate_links_item_id ON affiliate_links(item_id);

