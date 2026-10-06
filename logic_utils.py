"""Pure game logic for the Glitchy Guesser.

Everything in here is free of Streamlit so it can be unit-tested with pytest.
app.py only handles UI and session state and calls into these functions.
"""

DIFFICULTY_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    # FIXED: Hard used to be (1, 50), which made it *easier* than Normal.
    "Hard": (1, 200),
}

ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}

HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    # FIXED: these two messages were swapped. A guess that is too high
    # must tell the player to go LOWER, and vice versa.
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    return DIFFICULTY_RANGES.get(difficulty, DIFFICULTY_RANGES["Normal"])


def get_attempt_limit(difficulty: str) -> int:
    """Return how many guesses the player gets for a given difficulty."""
    return ATTEMPT_LIMITS.get(difficulty, ATTEMPT_LIMITS["Normal"])


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    If low/high are given, the guess must fall inside that inclusive range.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    raw = raw.strip()

    try:
        value = float(raw)
    except ValueError:
        return False, None, "That is not a number."

    # FIXED: decimals like "50.9" used to be silently truncated to 50.
    if not value.is_integer():
        return False, None, "Please enter a whole number."
    value = int(value)

    # FIXED: there was no range check, so guesses like -50 were accepted.
    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Your guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """
    Compare guess to secret and return the outcome.

    outcome is one of: "Win", "Too High", "Too Low"
    """
    # FIXED: app.py used to pass the secret in as a *string* on every
    # even attempt, which forced an alphabetical comparison ("9" > "80").
    # Both values are now always compared as integers.
    guess, secret = int(guess), int(secret)

    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def get_hint_message(outcome: str) -> str:
    """Return the hint text shown to the player for an outcome."""
    return HINT_MESSAGES[outcome]


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    attempt_number is 1-based: the first guess of a game is attempt 1.
    """
    if outcome == "Win":
        # FIXED: used `attempt_number + 1`, which took an extra 10 points
        # off every win. A first-try win is now worth the full 100.
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)

    # FIXED: "Too High" used to *add* 5 points on even attempts.
    # Every wrong guess now costs the same 5 points.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
