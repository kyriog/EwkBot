from random import random

def generate_kweh():
    text = []
    base_bonus = 0
    require_cap = True
    while base_bonus + random() <= 1.05:
        punctuation_score = random()
        if punctuation_score <= 0.3:
            punctuation = ""
            next_cap = False
        elif punctuation_score <= 0.6:
            punctuation = ","
            next_cap = False
        elif punctuation_score <= 0.8:
            punctuation = "."
            next_cap = True
        elif punctuation_score <= 0.9:
            punctuation = "?"
            next_cap = True
        else:
            punctuation = "!"
            next_cap = True
        text.append(f"{'K' if require_cap else 'k'}weh{punctuation}")
        require_cap = next_cap
        base_bonus += 0.1
    joined = " ".join(text)
    if joined.endswith(','):
        joined = joined[:-1] + "."
    elif not joined.endswith(('.', '?', '!')):
        joined += "."
    return joined
