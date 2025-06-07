# utils/word_tools.py
import re

def is_palindrome(word):
    cleaned = re.sub(r'[^a-zA-Z]', '', word.lower())
    return cleaned == cleaned[::-1] and len(cleaned) > 0

def is_valid_word(word, word_set):
    return word.lower() in word_set

def reverse_word(word):
    return word[::-1]

