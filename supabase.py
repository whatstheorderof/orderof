import os
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "https://vrojutbnratuonimkrpo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZyb2p1dGJucmF0dW9uaW1rcnBvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1ODIxNzMsImV4cCI6MjA2ODE1ODE3M30.XZjdN_J0OaeuTc2383dkrrrbwebFLQCyfIswFZLFOSM"

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client() -> Client:
    """Get the Supabase client instance."""
    return supabase

