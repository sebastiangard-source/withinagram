import requests
from services.database import get_rest_headers, SUPABASE_REST_URL

def fetch_user_submissions(user_id):
    url = f"{SUPABASE_REST_URL}/submissions?user_id=eq.{user_id}&order=timestamp.desc"
    response = requests.get(url, headers=get_rest_headers())
    if response.status_code == 200:
        return response.json()
    return []

def fetch_leaderboard():
    url = f"{SUPABASE_REST_URL}/submissions"
    response = requests.get(url, headers=get_rest_headers())
    if response.status_code != 200:
        return []

    all_submissions = response.json()
    name_counts = {}
    palindrome_counts = {}

    for row in all_submissions:
        username = row.get("username") or "Unknown"
        name_counts[username] = name_counts.get(username, 0) + 1

        reversed_word = row.get("reversed", "")
        if reversed_word and reversed_word == reversed_word[::-1]:
            palindrome_counts[username] = palindrome_counts.get(username, 0) + 1

    leaderboard = []
    for username, count in name_counts.items():
        pal_count = palindrome_counts.get(username, 0)
        pal_display = "🎉" * min(pal_count, 10) + ("..." if pal_count > 10 else "")
        leaderboard.append({
            "name": username,
            "count": count,
            "palindromes": pal_display
        })

    leaderboard.sort(key=lambda x: x["count"], reverse=True)
    return leaderboard
