import re

def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None


def is_stop_command(text):
    return any(word in text for word in ("stop", "wait", "cancel", "quiet"))


# SAME FUNCTION â€” JUST CLEAN PARAM NAME (NO LOGIC CHANGE)
def remove_words(query, words_to_remove):
    words = query.split()
    filtered_words = [word for word in words if word.lower() not in words_to_remove]
    result_string = ' '.join(filtered_words)
    return result_string