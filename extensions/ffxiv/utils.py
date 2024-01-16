from random import random, choice

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

def quote_emet():
    return choice([
        "No lands must remain beyond our grasp. Go forth. Conquer. Rule.",
        "I should be the one to sigh.",
        "I am Solus zos Galvus, founding father of the Garlean Empire. And, under various guises, the architect of myriad other imperially inclined nations. As for my true identity... I am Emet-Selch. Ascian.",
        "Just once...might we not seek to find common ground? For good or ill, I am immortal. Provided I have the inclination, I can always begin anew. Scheme and conspire to my heart's content.",
        "So come. Shed your preconceptions. See beyond the unscrupulous villains you take us for.",
        "You've committed the cardinal sin of boring me. And so I retire to the shade.",
        "Once you've found a likely spot, all you need do is whistle. You do know how to whistle, don't you, hero? Just put your lips together and blow. Well, what are you standing around here for? Get searching! You do want to save her, don't you?",
        "What a touching reunion that was. It fair brought a tear to the eye. But as we both know, such tender moments are nothing if not momentary. Before long, they will remember their many differences, and return to squabbling. ",
        "Oh, if I had a gil for every time one of you heroes made that claim...",
        "Ah hah hah! Flattery will get you nowhere, dear boy.",
        "Really. I have no need of deception─and even if I did, I assure you: you would find it quite indistinguishable from the truth.",
        "But conquest is the easy part. The true challenge begins once the dust has settled─quenching the glowing embers of animosity and maintaining a semblance of peace. This requires the conqueror to treat the conquered with dignity, and the conquered to let bygones be bygones. A difficult feat to achieve.",
        "What? You thought ancient beings like us incapable of crying? Well, rest assured that if your heart can be broken, then so can mine!",
        "Alas, it is not your grand scheme that will succeed, but ours.",
        "You cannot be entrusted with our legacy. I will bring back our brethren. Our friends. Our loved ones. The world belongs to us and us alone.",
        "Behold, the coming oblivion. 'Twas the end of our era, and the beginning of our great work.",
        "Fool. Who are you? No one. *Nothing.* Once I have reclaimed my heritage, my first act will be to expunge your stain from history's weave. My world will have no need for heroes.",
        "And you! Why waste your final moments in futile defiance? Weary wanderer─you've no fight left to fight! No life left to live!",
        "The victor shall write the tale, and the vanquished become its villain!",
        "Behold, a sorcerer of eld! Tremble before my glory!",
        "Should I surrender this fight, what will become of it all...? What will become of our triumphs? Our hopes? Our...our despair? What of this anguish which yet burns in my breast even after the passing of eons? No, no, no! I will not let it all be for naught!",
        "Remember... Remember us... Remember... that we once lived...",
        "Tell me, have you been to the ruins beneath the waters of the Bounty? Or the treasure islands beyond the frozen waters of Blindfrost, in Othard's north? The fabled golden cities of the New World? The sacred sites of the forgotten peoples of South Sea Isles? What about Meracydia, the southern continent? Do you know aught of its present state of affairs? I thought not. Even of your little Eorzea, you know precious little. The true identities of the Twelve, for instance. All of which is to say: expand your horizons. Go forth and seek discovery. Some of the civilizations in the reflections will surprise you. As the bearer of Azem's crystal, you may consider it duty to see at least that much. I certainly did.",
    ])
