# Music Recommender Simulation

## Original Project

My original Module project was **Music Recommender Simulation**. It was a small rule-based recommender that loaded songs from a CSV file, compared them to a user taste profile, and ranked the best matches. The goal was to show how an AI-style system can turn structured data into recommendations while staying simple enough to inspect, test, and explain.

## Title and Summary

This project demonstrates a transparent music recommendation system that scores songs based on genre, mood, energy, and acoustic preference. It matters because it shows the core ideas behind recommendation systems without hiding the logic inside a black box. A future employer can inspect the code, understand the trade-offs, and see that the project includes clear logging, testing, and documented behavior.

## Architecture Overview

The system is organized as a small pipeline:

1. The CLI runner in [src/main.py](src/main.py) loads the dataset and defines test user profiles.
2. The loader in [src/recommender.py](src/recommender.py) reads [data/songs.csv](data/songs.csv) and normalizes the song data.
3. The scoring engine evaluates every song against the user profile and produces a ranked list with explanations.
4. The terminal prints the top recommendations, and the tester/human reviewer checks whether the results make sense.
5. The pytest suite in [tests/test_recommender.py](tests/test_recommender.py) verifies ranking and explanation behavior.

The diagram in [assets/system_architecture.mmd](assets/system_architecture.mmd) shows the same flow visually, including where human review and automated testing fit into the loop.

## Setup Instructions

1. Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Run the application.

```bash
PYTHONPATH=. python -m src.main
```

4. Run the tests.

```bash
PYTHONPATH=. pytest -q
```

## Sample Interactions

These examples come from real runs of the application.

### Example 1: High-Energy Pop

Input profile:

```text
favorite_genre=pop
favorite_mood=happy
target_energy=0.9
likes_acoustic=False
```

Resulting output:

- Sunrise City - Neon Echo, final score 6.18, with genre match, mood match, energy closeness, and non-acoustic preference match
- Gym Hero - Max Pulse, final score 5.38
- Rooftop Lights - Indigo Parade, final score 4.94

This shows the system strongly prioritizes songs that fit the requested vibe.

### Example 2: Chill Lofi

Input profile:

```text
favorite_genre=lofi
favorite_mood=calm
target_energy=0.25
likes_acoustic=True
```

Resulting output:

- Library Rain - Paper Lanterns, final score 5.10, with genre match, energy closeness, and acoustic preference match
- Focus Flow - LoRoom, final score 4.90
- Midnight Coding - LoRoom, final score 4.82

This demonstrates that the recommender can adapt to a low-energy, acoustic-friendly preference.

### Example 3: Edge Case Profile

Input profile:

```text
favorite_genre=synthwave
favorite_mood=happy
target_energy=0.0
likes_acoustic=False
```

Resulting output:

- Velvet Strings - Orchid Chamber, final score 3.28
- Spacewalk Thoughts - Orbit Bloom, final score 2.88
- Sunday Fields - Golden Reed, final score 2.68

This example is useful because the genre is unknown, so the ranking falls back to energy similarity and still produces valid recommendations.

## Design Decisions

I built the system as a rule-based recommender instead of using a large machine learning model because the assignment emphasized clarity, reproducibility, and explanation. That choice makes the behavior easy to test and easy to describe in a portfolio setting. The trade-off is that the system cannot learn from large-scale user feedback, so it is less adaptive than a production recommender.

I also added logging, input clamping, and edge-case profiles because I wanted the project to behave reliably under unusual inputs. The trade-off is that the system is still intentionally simple and small-scale, but that simplicity makes the architecture easier to defend and review.

## Testing Summary

What worked well:

- The recommender consistently returned the expected top matches for normal profiles.
- The explanation strings clearly showed why each song was ranked.
- The edge-case and adversarial profiles helped confirm that the scoring logic still produced valid output.
- The pytest suite passed after the package/import setup was corrected.

What did not work at first:

- The first test run failed because the `src` package was not being resolved in the default Python path.
- Adding [src/__init__.py](src/__init__.py) and running with `PYTHONPATH=.` fixed the issue.

What I learned:

- Small validation tests are very useful for catching environment and import problems early.
- Explanation output matters almost as much as the ranking itself because it makes the system easier to trust and debug.

## Reflection

This project taught me that AI problem-solving is not just about producing an answer; it is also about making the system understandable, testable, and reliable. Even a simple recommender has to handle messy inputs, clear failure modes, and evaluation from both a human and a test suite.

It also showed me the value of trade-offs in AI design. A transparent rule-based system is easier to explain and maintain, while a more advanced model could be more flexible but harder to debug. For a portfolio project, I think the best choice is the one that clearly demonstrates reasoning, structure, and accountability.

## Screenshots and Assets

All screenshots and architecture files are stored in [assets](assets):

- [High-Energy Pop screenshot](assets/Screenshot%201.png)
- [Chill Lofi screenshot](assets/Screenshot%202.png)
- [Deep Intense Rock screenshot](assets/Screenshot%203.png)
- [Adversarial profile screenshot](assets/Screenshot%204.png)
- [Edge-case profile screenshot](assets/Screenshot%205.png)
- [Loaded song screenshot](assets/Screenshot_loaded_song.png)
- [System architecture diagram source](assets/system_architecture.mmd)

## Repository Contents

- [src](src): application logic and CLI entry point
- [data](data): song dataset
- [tests](tests): automated validation
- [assets](assets): screenshots and architecture files
- [model_card.md](model_card.md): model card discussion
- [reflection.md](reflection.md): reflection prompt responses

## Reliability & Evaluation

Automated tests:

- `pytest` unit tests included in `tests/test_recommender.py` validate ranking and explanation behavior. Current status: 2 passed, 0 failed.

Confidence scoring:

- Each recommendation includes a lightweight confidence score computed from the item's final score divided by an upper bound (max possible score = 6.5). This helps flag low-confidence recommendations when the system lacks strong matches.

Logging and guardrails:

- Numeric fields are clamped to [0,1] and malformed inputs fall back to safe defaults — warnings are logged when clamping occurs.
- The CLI exits cleanly with an error if `data/songs.csv` is missing or empty.

Human evaluation:

- The runner includes adversarial and edge-case profiles to surface failure modes for manual review.

Summary metric (sample run):

- Tests: 2 passed. Import issue fixed earlier by adding `src/__init__.py`.
- Average confidence across the evaluation run: 0.65 (values range 0.39–0.95). Lower confidences appear for unknown-genre or very-low-energy profiles.

Use these signals together: automated tests ensure core behavior, confidence scores and logs help triage failures, and human review validates explanation quality.

## Reflection and Ethics

**Limitations and biases:** Small dataset, hand-authored weights for genre/mood/energy, and a simplified user model that ignores long-term preferences. These design choices can bias toward certain genres or energy levels.

**Potential misuse:** An actor could craft profiles to promote specific content or exploit weighting biases. Mitigations: add content moderation, rate limits, and human review for any curated playlists. For production, audit for fairness and track dataset provenance.

**Surprising findings:** Energy similarity dominated when genres did not match, producing lower-confidence but reasonable recommendations. Environment/import issues took the most debugging time.

**AI collaboration:** Helpful suggestion was adding logging and guardrails, which improved reliability. A flawed suggestion targeted the wrong Python interpreter, causing test failures that required manual fix and switching interpreters.

Overall: responsible AI requires both technical measures (tests, logging, validation) and human oversight.

## Stretch Features (Bonus)

Three optional stretch features have been implemented for extra credit:

### 1. Test Harness or Evaluation Script (+2 points)

Run the comprehensive evaluation script:

```bash
PYTHONPATH=. python -m src.evaluate
```

This runs predefined test cases (normal, adversarial, edge-case profiles) and outputs:
- Pass/fail scores for each test
- Average confidence metrics
- Genre and mood match rates
- Overall system reliability summary

**Sample result:** Tests Passed: 4/4, Average Confidence: 0.69, Genre Match Rate: 58.3%

### 2. Agentic Workflow Enhancement (+2 points)

Run the multi-step reasoning demonstration:

```bash
PYTHONPATH=. python -m src.agent
```

This demonstrates an agentic workflow with three observable steps:
1. **Profile Classification:** Analyzes user preferences for complexity
2. **Strategy Selection:** Chooses scoring strategy based on profile type
3. **Recommendation Generation:** Returns top matches with interval reasoning

Example: An adversarial profile (high energy + sad mood) is detected and triggers a "simple" strategy prioritizing genre over conflicting mood.

### 3. Fine-Tuning/Specialization Modes (+2 points)

Run the specialization demonstration:

```bash
PYTHONPATH=. python -m src.specialize
```

Shows how the same user profile yields different recommendations based on context:
- **standard:** Balanced weighting across features (default)
- **study:** De-emphasized energy, prioritizes calm
- **workout:** Heavy energy emphasis, less genre-dependent
- **chill:** Prioritizes low energy and acoustic tracks

Example measurable difference: The same pop/happy profile produces average confidence 0.81 in standard mode but 0.98 in workout mode (different weight distributions).

To use specialization in code, pass `specialization_mode` in the user profile:

```python
profile = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.7,
    "likes_acoustic": False,
    "specialization_mode": "workout"  # Add this parameter
}
recommendations = recommend_songs(profile, songs, k=5)
```

