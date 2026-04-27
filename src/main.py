"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import logging
import sys

from .recommender import load_songs, recommend_songs


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

LOGGER = logging.getLogger(__name__)


def main() -> None:
    try:
        songs = load_songs("data/songs.csv")
    except FileNotFoundError as exc:
        LOGGER.error("Unable to start recommender: %s", exc)
        sys.exit(1)

    if not songs:
        LOGGER.error("No songs loaded from data/songs.csv. Exiting.")
        sys.exit(1)

    LOGGER.info("Loaded songs: %s", len(songs))

    profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.9,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "calm",
            "target_energy": 0.25,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "angry",
            "target_energy": 0.95,
            "likes_acoustic": False,
        },
        # System Evaluation: adversarial/edge-case profiles to probe scoring behavior.
        "Adversarial Conflict (High Energy + Sad)": {
            "favorite_genre": "pop",
            "favorite_mood": "sad",
            "target_energy": 0.9,
            "likes_acoustic": True,
        },
        "Edge Case: Unknown Genre + Very Low Energy": {
            "favorite_genre": "synthwave",
            "favorite_mood": "happy",
            "target_energy": 0.0,
            "likes_acoustic": False,
        },
    }

    print("\nSystem Evaluation: Top 5 recommendations per profile\n")
    for profile_name, taste_profile in profiles.items():
        recommendations = recommend_songs(taste_profile, songs, k=5)
        if not recommendations:
            LOGGER.warning("No recommendations generated for profile '%s'", profile_name)
            continue

        print(f"=== {profile_name} ===")
        for idx, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            reasons = [reason.strip() for reason in explanation.split(",") if reason.strip()]

            print(f"{idx}. {song['title']} - {song['artist']}")
            print(f"   Final score: {score:.2f}")
            print("   Reasons:")
            for reason in reasons:
                print(f"   - {reason}")
            print()


if __name__ == "__main__":
    main()
