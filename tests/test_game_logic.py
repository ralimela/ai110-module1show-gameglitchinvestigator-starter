from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_hint_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# ---------------------------------------------------------------------------
# Tests for the bugs fixed in Phase 2
# ---------------------------------------------------------------------------

# Bug: hints were backwards ("Too High" said "Go HIGHER!")
def test_too_high_hint_says_go_lower():
    assert get_hint_message(check_guess(60, 50)) == "📉 Go LOWER!"

def test_too_low_hint_says_go_higher():
    assert get_hint_message(check_guess(40, 50)) == "📈 Go HIGHER!"

def test_user_reported_case_65_vs_89_says_go_higher():
    # From the bug log: guessing 65 with a secret of 89 said "Go Lower".
    assert check_guess(65, 89) == "Too Low"
    assert get_hint_message(check_guess(65, 89)) == "📈 Go HIGHER!"


# Bug: secret was turned into a string on even attempts, so "9" > "80"
def test_string_secret_is_compared_as_a_number():
    # Alphabetically "9" > "80", but numerically 9 < 80.
    assert check_guess(9, "80") == "Too Low"
    assert check_guess("100", 99) == "Too High"
    assert check_guess(50, "50") == "Win"


# Bug: negative / out-of-range guesses were accepted
def test_negative_guess_is_rejected():
    ok, value, err = parse_guess("-50", 1, 100)
    assert ok is False
    assert value is None
    assert err == "Your guess must be between 1 and 100."

def test_guess_above_range_is_rejected():
    ok, _, _ = parse_guess("101", 1, 100)
    assert ok is False

def test_range_boundaries_are_accepted():
    assert parse_guess("1", 1, 100) == (True, 1, None)
    assert parse_guess("100", 1, 100) == (True, 100, None)


# Input parsing edge cases
def test_valid_guess_with_whitespace_is_parsed():
    assert parse_guess("  42 ", 1, 100) == (True, 42, None)

def test_empty_guess_is_rejected():
    assert parse_guess("", 1, 100) == (False, None, "Enter a guess.")
    assert parse_guess("   ", 1, 100) == (False, None, "Enter a guess.")
    assert parse_guess(None, 1, 100) == (False, None, "Enter a guess.")

def test_non_number_is_rejected():
    assert parse_guess("abc", 1, 100) == (False, None, "That is not a number.")

def test_decimal_guess_is_rejected_not_truncated():
    ok, value, _ = parse_guess("50.9", 1, 100)
    assert ok is False
    assert value is None

def test_whole_number_written_as_decimal_is_accepted():
    assert parse_guess("50.0", 1, 100) == (True, 50, None)


# Bug: Hard range (1-50) was easier than Normal (1-100)
def test_difficulty_ranges_get_harder():
    easy = get_range_for_difficulty("Easy")
    normal = get_range_for_difficulty("Normal")
    hard = get_range_for_difficulty("Hard")
    assert easy[1] < normal[1] < hard[1]

def test_attempt_limits():
    assert get_attempt_limit("Easy") == 6
    assert get_attempt_limit("Normal") == 8
    assert get_attempt_limit("Hard") == 5


# Bug: scoring was inconsistent
def test_first_try_win_scores_full_100():
    assert update_score(0, "Win", attempt_number=1) == 100

def test_win_score_never_drops_below_10():
    assert update_score(0, "Win", attempt_number=50) == 10

def test_wrong_guesses_always_cost_5_points():
    # "Too High" used to give +5 on even attempts.
    for attempt in range(1, 9):
        assert update_score(0, "Too High", attempt) == -5
        assert update_score(0, "Too Low", attempt) == -5
