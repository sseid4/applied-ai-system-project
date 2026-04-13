"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Concrete taste profile used for song comparisons
    taste_profile = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(taste_profile, songs, k=5)

    print("\nTop recommendations:\n")
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
