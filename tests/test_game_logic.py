from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_hint_direction_for_too_high_guess():
    """Regression test: a too-high guess should tell the player to go LOWER."""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message
