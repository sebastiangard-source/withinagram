import requests
from services.database import get_rest_headers, SUPABASE_REST_URL


def fetch_username(user_id, email=None):
    # Try to fetch by user_id
    url = f"{SUPABASE_REST_URL}/submissions?user_id=eq.{user_id}&order=id.desc&limit=1"
    response = requests.get(url, headers=get_rest_headers())
    if response.status_code == 200:
        data = response.json()
        if data and data[0].get("username"):
            return data[0]["username"]

    # Fallback by email
    if email:
        fallback_url = f"{SUPABASE_REST_URL}/submissions?email=eq.{email}&order=id.desc&limit=1"
        fallback = requests.get(fallback_url, headers=get_rest_headers())
        if fallback.status_code == 200:
            data = fallback.json()
            if data and data[0].get("username"):
                return data[0]["username"]

    return None
