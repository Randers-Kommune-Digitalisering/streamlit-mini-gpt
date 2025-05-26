import re


def parse_filename(text: str) -> str:
    """
    Remove special characters except dash, underscore, dot, and space, as well as non-latin characters.
    Only keeps a-z, A-Z, 0-9, dash (-), underscore (_), dot (.), and space.
    """
    text = replace_danish_characters(text)
    return re.sub(r'[^a-zA-Z0-9\-_. ]', '', text)


def replace_danish_characters(text: str) -> str:
    replacements = {
        'æ': 'ae',
        'ø': 'oe',
        'å': 'aa',
        'Æ': 'AE',
        'Ø': 'OE',
        'Å': 'AA'
    }
    for danish_char, english_char in replacements.items():
        text = text.replace(danish_char, english_char)
    return text
