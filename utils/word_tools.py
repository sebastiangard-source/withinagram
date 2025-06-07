import re
from datetime import datetime
from services.database import supabase
from utils.helpers import is_valid_word, is_palindrome, format_timestamp

def reverse_word(word):
    return word[::-1]

def is_palindrome(word):
    cleaned = re.sub(r'[^a-zA-Z]', '', word.lower())
    return cleaned == cleaned[::-1] and len(cleaned) > 0

def is_valid_word(word, word_set):
    return word.lower() in word_set

def process_submission(word, user_id, email, username, word_set):
    reversed_word = reverse_word(word)
    pal = is_palindrome(word)
    is_valid = is_valid_word(word, word_set)

    data = {
        "input": word,
        "reversed": reversed_word,
        "user_id": user_id,
        "email": email,
        "username": username,
        "timestamp": datetime.utcnow().isoformat(),
    }

    supabase.table("submissions").insert(data).execute()

    # Return emoji if it's a palindrome and valid word
    celebrate = " 🎉" if pal and is_valid else ""
    return reversed_word + celebrate
