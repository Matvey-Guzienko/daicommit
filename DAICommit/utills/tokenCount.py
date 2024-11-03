import tiktoken

def token_count(content: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(content)
    return len(tokens)
