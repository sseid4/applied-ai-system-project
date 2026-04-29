"""
Specialization Modes Demonstration for Music Recommender.

This script demonstrates how the same user preference yields different recommendations
depending on the context (study, workout, chill) using specialized weight adjustments.

Stretch Feature: Fine-Tuning or Specialization (+2 points)
"""

import logging
import sys

from .recommender import load_songs, recommend_songs, _compute_confidence

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

LOGGER = logging.getLogger(__name__)


def run_specialization_demo():
    """Demonstrate how specialization modes adapt the recommender."""
    try:
        songs = load_songs("data/songs.csv")
    except FileNotFoundError as exc:
        LOGGER.error("Unable to load songs: %s", exc)
        sys.exit(1)

    if not songs:
        LOGGER.error("No songs loaded. Exiting.")
        sys.exit(1)

    LOGGER.info("Loaded %d songs.", len(songs))

    # Base profile: a user who likes pop and happy vibes.
    base_profile = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.7,
        "likes_acoustic": False,
    }

    # Three specialization modes: standard, study, workout.
    modes = ["standard", "study", "workout", "chill"]

    print("\n" + "="*80)
    print("SPECIALIZATION MODES COMPARISON")
    print("="*80 + "\n")
    print("Base Profile (same for all modes):")
    print(f"  Genre: {base_profile['favorite_genre']}")
    print(f"  Mood: {base_profile['favorite_mood']}")
    print(f"  Target Energy: {base_profile['target_energy']}")
    print(f"  Likes Acoustic: {base_profile['likes_acoustic']}\n")

    mode_descriptions = {
        "standard": "Default scoring: balanced across genre, mood, energy.",
        "study": "Optimized for focus: de-emphasizes extreme energy, priorities calm.",
        "workout": "Optimized for exercise: heavy emphasis on energy, less genre-dependent.",
        "chill": "Optimized for relaxation: prioritizes low energy and acoustic tracks.",
    }

    results_by_mode = {}

    for mode in modes:
        print(f"\n{'─'*80}")
        print(f"MODE: {mode.upper()}")
        print(f"Description: {mode_descriptions[mode]}")
        print(f"{'─'*80}\n")

        # Add specialization mode to profile.
        profile = {**base_profile, "specialization_mode": mode}
        recommendations = recommend_songs(profile, songs, k=3)

        if not recommendations:
            print("  ❌ No recommendations generated.\n")
            continue

        print("Top 3 Recommendations:\n")
        confidences = []
        for idx, (song, score, explanation) in enumerate(recommendations, 1):
            conf = _compute_confidence(score)
            confidences.append(conf)
            print(f"{idx}. {song['title']} - {song['artist']}")
            print(f"   Score: {score:.2f}, Confidence: {conf:.2f}")
            print(f"   Energy: {song['energy']}, Acousticness: {song['acousticness']}")
            print(f"   Reasoning: {explanation}\n")

        avg_conf = sum(confidences) / len(confidences)
        results_by_mode[mode] = {
            "recommendations": recommendations,
            "avg_confidence": avg_conf,
        }

    # Summary comparison.
    print("="*80)
    print("SPECIALIZATION IMPACT SUMMARY")
    print("="*80 + "\n")
    print("Comparison of average confidence across modes:\n")

    for mode in modes:
        if mode in results_by_mode:
            avg_conf = results_by_mode[mode]["avg_confidence"]
            first_track = results_by_mode[mode]["recommendations"][0][0]["title"]
            print(f"  {mode:12s}: avg_confidence={avg_conf:.2f}  →  top track: {first_track}")
    
    print("\n✅ Specialization demonstration complete.")
    print("   Notice how different modes select different top recommendations")
    print("   based on context-specific weight adjustments.\n")


if __name__ == "__main__":
    run_specialization_demo()
