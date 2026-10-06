# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`
3. Run the tests: `python -m pytest -v`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

### The game's purpose

Glitchy Guesser is a number guessing game built with Streamlit. The game picks a secret number in a range set by the difficulty: **Easy** is 1–20 with 6 attempts, **Normal** is 1–100 with 8 attempts, and **Hard** is 1–200 with 5 attempts. After each guess, the player gets a hint telling them to go higher or lower. The goal is to find the number before running out of attempts. The score starts at 100 for a first-try win and drops by 10 for each extra guess, with a minimum of 10. Each wrong guess also costs 5 points. The starter code was written by an AI and was full of bugs. My job was to find them, fix them, and prove the fixes with tests.

### Bugs I found

| # | Bug | What I saw | Root cause |
|---|-----|-----------|------------|
| 1 | **Hints were backwards** | Guessing 65 with a secret of 89 told me "Go Lower" | The "Go HIGHER!" and "Go LOWER!" messages in `check_guess` were swapped. |
| 2 | **Hints were sometimes nonsense** | Hints were wrong even after taking bug 1 into account | On every even-numbered attempt, `app.py` turned the secret into a string. `check_guess` then compared text alphabetically, so `"9" > "80"`. |
| 3 | **"New Game" did nothing** | The game kept saying "Game over" after I clicked New Game | New Game never reset `status` (it stayed `"lost"`), `score` or `history`, and it picked the secret from 1–100 whatever the difficulty. |
| 4 | **Attempts counter was off** | It started at 7 instead of 8, didn't change on the first submit, and ended at "1 left" | `attempts` started at 1 instead of 0. The "Attempts left" box was also drawn before the guess was processed, so it always showed the previous turn. |
| 5 | **Debug info lagged one guess behind** | My first guess only showed up in History after my second guess | Same ordering problem: the debug panel was drawn before the guess was added to `history`. |
| 6 | **Negative and out-of-range guesses were accepted** | -50 was accepted and told me "Go Lower" | `parse_guess` never checked the guess against the difficulty's range. |
| 7 | **Hard was easier than Normal** | Hard's range was smaller than Normal's | Hard was set to 1–50 while Normal was 1–100. |
| 8 | **Other bugs** | — | The prompt always said "between 1 and 100". Decimals like 50.9 were cut down to 50. "Too High" *added* 5 points on even attempts. Invalid input used up an attempt. |

### Fixes I applied

- **Refactor:** I moved all game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) from `app.py` into `logic_utils.py`. Now `app.py` only handles the UI and session state, and the logic can be tested with pytest.
- **Hints:** I fixed the swapped messages and removed the string conversion. `check_guess` always compares integers and returns only the outcome (`"Win"`, `"Too High"` or `"Too Low"`). A new `get_hint_message()` function provides the hint text.
- **New Game:** a new `start_new_game()` function resets the secret (inside the current difficulty's range), attempts, score, status and history. Changing the difficulty also starts a new game.
- **Attempts and debug display:** attempts now start at 0 and only valid guesses count. The info box and debug panel use `st.empty()` placeholders that are filled in *after* the guess is processed, so they always show the current turn.
- **Input checks:** `parse_guess` rejects guesses outside the range, decimals, empty input and non-numbers, each with a clear error message.
- **Difficulty and scoring:** Hard is now 1–200. The range shown on screen matches the difficulty. Every wrong guess costs 5 points, and a first-try win is worth 100.
- **Tests:** I added 17 pytest tests in `tests/test_game_logic.py`, one or more per bug, on top of the 3 starter tests. I also added `pytest.ini` so the tests can import `logic_utils.py`.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (range 1–100, 8 attempts). The secret number is **63**:

1. The game starts and shows "Guess a number between 1 and 100. Attempts left: 8". Score is 0.
2. User enters **40** → the game shows **"📈 Go HIGHER!"**. Attempts left drops to **7** right away, and the debug History shows `[40]`. Score: **-5**.
3. User enters **80** → **"📉 Go LOWER!"**. Attempts left: **6**. Score: **-10**.
4. User enters **-5** → error: **"Your guess must be between 1 and 100."** No attempt is used (still **6**), and the score stays at -10.
5. User enters **abc** → error: **"That is not a number."** Still **6** attempts left.
6. User enters **60** → **"📈 Go HIGHER!"**. Attempts left: **5**. Score: **-15**.
7. User enters **63** → **"🎉 Correct!"**, balloons, and **"You won! The secret was 63. Final score: 55"**. This was the 4th valid guess: 70 win points minus 15 points for the 3 wrong guesses.
8. User tries another guess → "You already won. Start a new game to play again." The guess is ignored.
9. User clicks **New Game 🔁** → "New game started." Attempts left goes back to **8**, the score to **0**, History is empty, and there is a new secret.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest -v
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
rootdir: E:\Codepath\ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
testpaths: tests
collected 20 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  5%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 10%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 15%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED        [ 20%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED        [ 25%]
tests/test_game_logic.py::test_user_reported_case_65_vs_89_says_go_higher PASSED [ 30%]
tests/test_game_logic.py::test_string_secret_is_compared_as_a_number PASSED [ 35%]
tests/test_game_logic.py::test_negative_guess_is_rejected PASSED         [ 40%]
tests/test_game_logic.py::test_guess_above_range_is_rejected PASSED      [ 45%]
tests/test_game_logic.py::test_range_boundaries_are_accepted PASSED      [ 50%]
tests/test_game_logic.py::test_valid_guess_with_whitespace_is_parsed PASSED [ 55%]
tests/test_game_logic.py::test_empty_guess_is_rejected PASSED            [ 60%]
tests/test_game_logic.py::test_non_number_is_rejected PASSED             [ 65%]
tests/test_game_logic.py::test_decimal_guess_is_rejected_not_truncated PASSED [ 70%]
tests/test_game_logic.py::test_whole_number_written_as_decimal_is_accepted PASSED [ 75%]
tests/test_game_logic.py::test_difficulty_ranges_get_harder PASSED       [ 80%]
tests/test_game_logic.py::test_attempt_limits PASSED                     [ 85%]
tests/test_game_logic.py::test_first_try_win_scores_full_100 PASSED      [ 90%]
tests/test_game_logic.py::test_win_score_never_drops_below_10 PASSED     [ 95%]
tests/test_game_logic.py::test_wrong_guesses_always_cost_5_points PASSED [100%]

============================= 20 passed in 0.02s ==============================
```

The edge-case tests cover negative numbers, numbers above the range, the exact range limits (1 and 100), decimals ("50.9" is rejected, "50.0" is accepted), empty or whitespace-only input, non-numbers, a secret stored as a string, and the score never dropping below the 10-point minimum.

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
