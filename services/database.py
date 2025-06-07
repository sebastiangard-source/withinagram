import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY: str = os.getenv("SUPABASE_API_KEY")
SUPABASE_AUTH_URL: str = f"{SUPABASE_URL}/auth/v1"
SUPABASE_REST_URL: str = f"{SUPABASE_URL}/rest/v1"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def get_rest_headers():
    return {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }
