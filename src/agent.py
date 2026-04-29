"""
Agentic Workflow Runner for Music Recommender.

This script demonstrates the agentic workflow feature: multi-step reasoning
with observable intermediate steps (classification, strategy selection, recommendation).

Stretch Feature: Agentic Workflow Enhancement (+2 points)
"""

import logging
import sys

from .recommender import (
    load_songs,
    recommend_songs,
    _classify_profile_difficulty,
    _compute_confidence,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

LOGGER = logging.getLogger(__name__)


def run_agentic_workflow():
    """Run the recommender with multi-step agentic reasoning."""
    try:
        songs = load_songs("data/songs.csv")
    except FileNotFoundError as exc:
        LOGGER.error("Unable to load songs: %s", exc)
        sys.exit(1)

    if not songs:
        LOGGER.error("No songs loaded. Exiting.")
        sys.exit(1)

    LOGGER.info("Loaded %d songs.", len(songs))

    # Test profiles covering different complexity levels.
    profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.9,
            "likes_acoustic": False,
        },
        "Adversarial Conflict": {
            "favorite_genre": "pop",
            "favorite_mood": "sad",
            "target_energy": 0.9,
            "likes_acoustic": True,
        },
        "Edge Case (Unknown Genre)": {
            "favorite_genre": "synthwave",
            "favorite_mood": "happy",
            "target_energy": 0.0,
            "likes_acoustic": False,
        },
    }

    print("\n" + "="*80)
    print("AGENTIC WORKFLOW DEMONSTRATION")
    print("="*80 + "\n")

    for profile_name, user_prefs in profiles.items():
        print(f"User Profile: {profile_name}\n")

        # ============ AGENTIC STEP 1: Profile Classification ============
        print("AGENT REASONING:")
        difficulty, reasoning_steps = _classify_profile_difficulty(user_prefs)
        for step in reasoning_steps:
            print(f"  {step}")
        print(f"  ➜ Profile Classified As: {difficulty.upper()}\n")

        # ============ AGENTIC STEP 2: Recommendation Generation ============
        print("AGENT ACTION: Generating recommendations using selected strategy...\n")
        recommendations = recommend_songs(user_prefs, songs, k=3)

        if not recommendations:
            print("  ❌ No recommendations generated.\n")
            continue

        # ============ AGENTIC STEP 3: Results & Explanations ============
        print("AGENT RESULTS:\n")
        for idx, (song, score, explanation) in enumerate(recommendations, 1):
            conf = _compute_confidence(score)
            print(f"{idx}. {song['title']} - {song['artist']}")
            print(f"   Score: {score:.2f}, Confidence: {conf:.2f}")
            print(f"   Reasoning: {explanation}\n")

        print("-" * 80 + "\n")

    print("="*80)
    print("✅ Agentic workflow demonstration complete.\n")


if __name__ == "__main__":
    run_agentic_workflow()
