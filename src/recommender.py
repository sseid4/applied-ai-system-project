import csv
import logging
from typing import List, Dict, Tuple
from dataclasses import dataclass


LOGGER = logging.getLogger(__name__)


def _clamp_01(value: float, field_name: str) -> float:
    """Clamp values into [0, 1] and log when data is out of expected range."""
    if value < 0.0 or value > 1.0:
        LOGGER.warning("%s=%s out of range; clamping to [0,1]", field_name, value)
    return max(0.0, min(1.0, value))


def _to_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

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
        if k <= 0:
            return []

        scored: List[Tuple[Song, float]] = []
        user_dict = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

        for song in self.songs:
            score, _ = score_song(user_dict, {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "acousticness": song.acousticness,
            })
            scored.append((song, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = score_song(
            {
                "favorite_genre": user.favorite_genre,
                "favorite_mood": user.favorite_mood,
                "target_energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            },
            {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "acousticness": song.acousticness,
            },
        )
        return f"Score {score:.2f}: " + ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return typed song dictionaries."""
    songs: List[Dict] = []

    def parse_number(value: str):
        """Parse a numeric CSV field into int or float."""
        if "." in value:
            return float(value)
        return int(value)

    try:
        with open(csv_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                song = {
                    "id": parse_number(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": _clamp_01(_to_float(row.get("energy"), 0.0), "energy"),
                    "tempo_bpm": _to_float(row.get("tempo_bpm"), 0.0),
                    "valence": _clamp_01(_to_float(row.get("valence"), 0.0), "valence"),
                    "danceability": _clamp_01(_to_float(row.get("danceability"), 0.0), "danceability"),
                    "acousticness": _clamp_01(_to_float(row.get("acousticness"), 0.0), "acousticness"),
                }
                songs.append(song)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Songs CSV not found: {csv_path}") from exc

    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return score plus reasons."""
    score = 0.0
    reasons: List[str] = []

    # Sensitivity experiment: halve genre impact and double energy impact.
    genre_weight = 1.0
    mood_weight = 1.0
    energy_weight = 4.0

    favorite_genre = str(user_prefs.get("favorite_genre", user_prefs.get("genre", ""))).strip().lower()
    favorite_mood = str(user_prefs.get("favorite_mood", user_prefs.get("mood", ""))).strip().lower()
    target_energy = _clamp_01(_to_float(user_prefs.get("target_energy", user_prefs.get("energy", 0.5)), 0.5), "target_energy")
    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))

    song_genre = str(song.get("genre", "")).strip().lower()
    song_mood = str(song.get("mood", "")).strip().lower()
    song_energy = _clamp_01(_to_float(song.get("energy", 0.0), 0.0), "song.energy")
    song_acousticness = _clamp_01(_to_float(song.get("acousticness", 0.0), 0.0), "song.acousticness")

    if song_genre == favorite_genre and favorite_genre:
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight:.1f})")

    if song_mood == favorite_mood and favorite_mood:
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight:.1f})")

    energy_diff = abs(song_energy - target_energy)
    energy_points = max(0.0, energy_weight * (1.0 - energy_diff))
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    if likes_acoustic and song_acousticness >= 0.6:
        score += 0.5
        reasons.append("acoustic preference match (+0.5)")
    elif (not likes_acoustic) and song_acousticness <= 0.4:
        score += 0.5
        reasons.append("non-acoustic preference match (+0.5)")

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
