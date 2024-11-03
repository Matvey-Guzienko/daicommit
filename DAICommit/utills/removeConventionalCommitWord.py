import re

def remove_conventional_commit_word(message: str) -> str:
    return re.sub(r'^(fix|feat)\((.+?)\):', r'(\2):', message)
