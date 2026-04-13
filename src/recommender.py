import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return typed song dictionaries."""
    songs: List[Dict] = []

    def parse_number(value: str):
        """Parse a numeric CSV field into int or float."""
        if "." in value:
            return float(value)
        return int(value)

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song = {
                "id": parse_number(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": parse_number(row["energy"]),
                "tempo_bpm": parse_number(row["tempo_bpm"]),
                "valence": parse_number(row["valence"]),
                "danceability": parse_number(row["danceability"]),
                "acousticness": parse_number(row["acousticness"]),
            }
            songs.append(song)

    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return score plus reasons."""
    score = 0.0
    reasons: List[str] = []

    favorite_genre = user_prefs.get("favorite_genre", user_prefs.get("genre", ""))
    favorite_mood = user_prefs.get("favorite_mood", user_prefs.get("mood", ""))
    target_energy = float(user_prefs.get("target_energy", user_prefs.get("energy", 0.5)))

    if song.get("genre") == favorite_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song.get("mood") == favorite_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_diff = abs(float(song.get("energy", 0.0)) - target_energy)
    energy_points = max(0.0, 2.0 * (1.0 - energy_diff))
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score and return the top-k recommendations with explanations."""
    scored_songs: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]
