import random
import streamlit as st

# FIXED: the game logic used to live in this file, mixed in with the UI.
# It now lives in logic_utils.py so it can be unit-tested with pytest.
from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_hint_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def start_new_game(low: int, high: int):
    """Reset every piece of per-game session state."""
    # FIXED: "New Game" used to reset only `attempts` and `secret`. `status`
    # stayed "lost", so the app hit st.stop() forever. score and history were
    # never cleared, and the secret ignored the difficulty's range.
    st.session_state.secret = random.randint(low, high)
    # FIXED: attempts used to start at 1, which cost the player a guess.
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = get_attempt_limit(difficulty)
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Start a fresh game on first load, and whenever the difficulty changes, so
# the secret always falls inside the current range.
if st.session_state.get("difficulty") != difficulty:
    st.session_state.difficulty = difficulty
    start_new_game(low, high)

st.subheader("Make a guess")

# FIXED: the info box and debug panel used to be drawn *before* the guess was
# processed, so they always showed the previous turn's values. We reserve
# their spots on the page here and fill them in at the bottom of the script.
info_slot = st.empty()
debug_slot = st.empty()

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_game(low, high)
    st.success("New game started.")

if submit and st.session_state.status == "playing":
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        # FIXED: invalid input no longer uses up an attempt.
        st.error(err)
    else:
        # FIXED: attempts are only counted for valid guesses.
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIXED: removed the code that turned the secret into a string on
        # even attempts. check_guess now always compares two ints.
        outcome = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(get_hint_message(outcome))

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )
elif st.session_state.status == "won":
    st.success("You already won. Start a new game to play again.")
elif st.session_state.status == "lost":
    st.error("Game over. Start a new game to try again.")

# Everything has been updated for this turn, so draw the up-to-date values.
# FIXED: the range used to be hardcoded as "1 and 100" for every difficulty.
info_slot.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with debug_slot.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
