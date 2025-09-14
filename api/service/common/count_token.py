import tiktoken


def count_tokens(text: str) -> int:
    """
    Count tokens in the provided text and return detailed token information

    Args:
        text (str): The text to analyze

    Returns:
        token_count (int): The number of tokens in the text
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    token_count = len(tokens)

    # Create a list to hold the token representations
    #token_representations = []
    #for token in tokens:
    #    # Decode each token individually to its text representation
    #    token_text = encoding.decode([token])
    #    token_representations.append({"token_id": int(token), "token_text": token_text})

    return token_count
