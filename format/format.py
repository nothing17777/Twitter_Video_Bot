import re

ANIME_MAP = {
    # --- Chainsaw Man ---
    "chainsawman": "ChainsawMan",
    "chainsaw": "ChainsawMan",

    # --- Jujutsu Kaisen ---
    "jujutsu": "JujutsuKaisen",
    "jujutsukaisen": "JujutsuKaisen",

    # --- Demon Slayer ---
    "demonslayer": "DemonSlayer",
    "kimetsu": "KimetsuNoYaiba",
    "kimetsunoyaiba": "KimetsuNoYaiba",
    "demon slayer": "DemonSlayer",
    
    # --- Attack on Titan ---
    "aot": "AttackOnTitan",
    "attackontitan": "AttackOnTitan",
    "shingeki": "ShingekiNoKyojin",

    # --- My Hero Academia ---
    "mha": "MyHeroAcademia",
    "myhero": "MyHeroAcademia",
    "myheroacademia": "MyHeroAcademia",

    # --- Naruto ---
    "naruto": "Naruto",
    "shippuden": "NarutoShippuden",

    # --- One Piece ---
    "onepiece": "OnePiece",

    # --- Bleach ---
    "bleach": "Bleach",

    # --- Dragon Ball ---
    "dragonball": "DragonBall",
    "dragonballz": "DragonBallZ",
    "dbz": "DragonBallZ",

    # --- Tokyo Ghoul ---
    "tokyoghoul": "TokyoGhoul",

    # --- Death Note ---
    "deathnote": "DeathNote",

    # --- Monogatari ---
    "monogatari": "Monogatari",
    "bakemonogatari": "Bakemonogatari",

    # --- Evangelion ---
    "evangelion": "NeonGenesisEvangelion",
    "nge": "NeonGenesisEvangelion",

    # --- Fate ---
    "fate": "FateSeries",
    "fatezero": "FateZero",
    "fatestaynight": "FateStayNight",

    # --- Sword Art Online ---
    "sao": "SwordArtOnline",
    "swordartonline": "SwordArtOnline",

    # --- Blue Lock ---
    "bluelock": "BlueLock",

    # --- Haikyuu ---
    "haikyuu": "Haikyuu",

    # --- Spy x Family ---
    "spyxfamily": "SpyXFamily",

    # --- Oshi no Ko ---
    "oshinoko": "OshiNoKo",

    # --- Cyberpunk ---
    "cyberpunk": "CyberpunkEdgerunners",

    # --- Solo Leveling ---
    "sololeveling": "SoloLeveling",
}

JUNK_WORDS = {
    "clip", "clips", "edit", "edits", "amv",
    "anime", "video", "videos"
}

def camel(words):
    return "".join(w.capitalize() for w in words)


def hashtag_from_query(query):
    query = query.lower().strip()

    words = re.findall(r"[a-z]+", query)
    words = [w for w in words if w not in JUNK_WORDS]

    anime_tag = None

    # find first matching anime in query
    for word in words:
        if word in ANIME_MAP:
            anime_tag = ANIME_MAP[word]
            break

    # fallback: just capitalize first word
    if anime_tag is None and words:
        anime_tag = words[0].capitalize()

    if anime_tag:
        return [f"#{anime_tag}", "#Anime"]

    return ["#Anime"]

if __name__ == "__main__":
    print(hashtag_from_query("chainsawman reze dance clip"))