"""
Test Harness and Evaluation Script for Music Recommender.

This script runs the recommender against predefined test cases,
collects metrics, and outputs a comprehensive evaluation report.

Stretch Feature: Test Harness or Evaluation Script (+2 points)
"""

import logging
import sys
from typing import Dict, List, Tuple

from .recommender import load_songs, recommend_songs, _compute_confidence

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

LOGGER = logging.getLogger(__name__)


def run_evaluation():
    """Run a comprehensive test harness on the recommender."""
    try:
        songs = load_songs("data/songs.csv")
    except FileNotFoundError as exc:
        LOGGER.error("Unable to load songs: %s", exc)
        sys.exit(1)

    if not songs:
        LOGGER.error("No songs loaded. Exiting.")
        sys.exit(1)

    LOGGER.info("Loaded %d songs for evaluation.", len(songs))

    # Define predefined test cases covering normal, adversarial, and edge cases.
    test_cases = {
        "normal_pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.9,
            "likes_acoustic": False,
            "expected_characteristics": "should have high confidence, genre/mood matches",
        },
        "normal_lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "calm",
            "target_energy": 0.25,
            "likes_acoustic": True,
            "expected_characteristics": "should have high confidence, acoustic preference match",
        },
        "adversarial_conflict": {
            "favorite_genre": "pop",
            "favorite_mood": "sad",
            "target_energy": 0.9,
            "likes_acoustic": True,
            "expected_characteristics": "conflicting mood/energy, moderate confidence",
        },
        "edge_unknown_genre": {
            "favorite_genre": "synthwave",
            "favorite_mood": "happy",
            "target_energy": 0.0,
            "likes_acoustic": False,
            "expected_characteristics": "unknown genre, should fallback to energy matching, lower confidence",
        },
    }

    # Collect results and metrics.
    results = {}
    all_confidences = []
    passed_tests = 0
    total_tests = len(test_cases)

    print("\n" + "="*80)
    print("MUSIC RECOMMENDER EVALUATION REPORT")
    print("="*80 + "\n")

    for test_name, profile in test_cases.items():
        print(f"Test Case: {test_name}")
        print(f"  Expected: {profile['expected_characteristics']}")

        recommendations = recommend_songs(profile, songs, k=3)

        if not recommendations:
            print(f"  ❌ FAIL: No recommendations generated.\n")
            continue

        # Extract and analyze metrics.
        confidences = []
        genre_matches = 0
        mood_matches = 0

        for song, score, explanation in recommendations:
            conf = _compute_confidence(score)
            confidences.append(conf)
            all_confidences.append(conf)

            if song["genre"].lower() == profile["favorite_genre"].lower():
                genre_matches += 1
            if song["mood"].lower() == profile["favorite_mood"].lower():
                mood_matches += 1

        avg_conf = sum(confidences) / len(confidences)
        genre_match_rate = genre_matches / len(recommendations)
        mood_match_rate = mood_matches / len(recommendations)

        # Simple pass/fail logic based on test type.
        passed = False
        if test_name.startswith("normal"):
            passed = avg_conf >= 0.75 and (genre_match_rate > 0.0 or mood_match_rate > 0.0)
        elif test_name.startswith("adversarial"):
            passed = avg_conf >= 0.50 and len(recommendations) > 0
        elif test_name.startswith("edge"):
            passed = avg_conf >= 0.40 and len(recommendations) > 0

        status = "✅ PASS" if passed else "⚠️  WARN"
        if passed:
            passed_tests += 1

        print(f"  {status}")
        print(f"    Top recommendation: {recommendations[0][0]['title']}")
        print(f"    Average confidence: {avg_conf:.2f}")
        print(f"    Genre match rate: {genre_match_rate:.1%}")
        print(f"    Mood match rate: {mood_match_rate:.1%}\n")

        results[test_name] = {
            "avg_confidence": avg_conf,
            "genre_match_rate": genre_match_rate,
            "mood_match_rate": mood_match_rate,
            "passed": passed,
        }

    # Print overall summary.
    print("="*80)
    print("SUMMARY METRICS")
    print("="*80)
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print(f"Overall Average Confidence: {sum(all_confidences) / len(all_confidences):.2f}")
    print(f"Confidence Range: [{min(all_confidences):.2f}, {max(all_confidences):.2f}]")
    print(f"Genre Match Rate (global): {sum(r['genre_match_rate'] for r in results.values()) / len(results):.1%}")
    print(f"Mood Match Rate (global): {sum(r['mood_match_rate'] for r in results.values()) / len(results):.1%}")
    print("\n✅ Evaluation complete.\n")


if __name__ == "__main__":
    run_evaluation()
