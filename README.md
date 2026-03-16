# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
   - This app is a Streamlit number guessing game where the player tries to guess a secret number within a limited number of attempts, using higher/lower hints.

- [x] Detail which bugs you found.
   - Hints were incorrect/inconsistent (e.g., a too-high guess could still tell me to go higher, and hints could flip between attempts).
   - Clicking **New Game** could leave the app in a stuck state after winning/losing (it wouldn’t let me keep guessing).
   - The UI text always said the guess range was 1–100 even when difficulty changed the actual range.

- [x] Explain what fixes you applied.
   - Refactored the core game logic into `logic_utils.py` so logic is shared between the Streamlit app and pytest.
   - Fixed `check_guess` so it returns the correct hint direction (Too High → LOWER, Too Low → HIGHER) using consistent numeric comparison.
   - Updated the **New Game** handler to reset the relevant `st.session_state` values (status/score/history/secret) so a fresh game starts immediately.
   - Added/updated pytest coverage (including a small regression test) and confirmed all tests pass.

## 📸 Demo

- 

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
