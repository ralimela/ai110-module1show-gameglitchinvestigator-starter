# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

As I enter my first guess such as 65 and clicked submit it gave me a hint to go lower. As I kept guessing lower number, it kept telling me to go lower and eventually I was out of attempts and the actual answer was higher than my first guess and the hints took me completely on the wrong track. Also when i click the "New Game" button, it doesn't work and just keeps saying that I am out of attempts. The hints were never accurate and they were in fact giving the opposite hints. I alse see that when I hit "submit answer" button, the guess doesn't reflect immediately in the developer debug info section and when I put in the second attempt, thats when the first guess shows up in the debug section. The last error that I saw is that the attempts left shows 7 to begin with and when i hit the first submit, it still stays at 7 and it goes down to 1 attampt left and says "Out of attempts!". I am sure there is an error in the attempts counting function of the code. The game also accepts negative guesses such as -50 and also says "Go Lower" funnily. 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|65(89) | Go Higher         | Go Lower        | Out of attempts! The secret was 89. Score: -35
| 5(79) | Go Lower          | Go Higher       | None
|-50(75)| Go Lower          | Go Higher       | None

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

**Tools used:** I used Claude Code (Claude Opus 5.5) inside VS Code in agent mode. I gave it my bug notes from section 1 and asked it to find the logic behind each bug. Then I asked it to refactor and fix the code and write pytest tests. The game itself was also written by an AI, so I treated the starter code as "AI suggestions" to review too.

**A suggestion that was correct: why my hints were wrong.** I had guessed that the hints were just reversed. Claude found two separate causes. First, the "Go HIGHER!" and "Go LOWER!" messages in `check_guess` were swapped. Second, on every even-numbered attempt `app.py` turned the secret into a string with `str(st.session_state.secret)`. That made `check_guess` hit a `TypeError` and fall back to comparing text alphabetically, where `"9" > "80"` is `True`. Attempts started at 1 and were increased before the check, so my very first guess was always one of these string comparisons. That explains why 65 against 89 said "Go Lower". This was correct because it explained every wrong hint in my log, not just some of them. I verified it with the pytest case `test_user_reported_case_65_vs_89_says_go_higher` (guess 65, secret 89 → "Too Low" / "Go HIGHER!"). I also checked it with `test_string_secret_is_compared_as_a_number`, which checks that `check_guess(9, "80")` returns "Too Low". Both pass, and in a replay of the game, 65 against 89 now says "Go HIGHER!" on the first guess.

**A suggestion I did not accept as written: the starter's `check_guess` design.** The AI-written starter code had `check_guess` return a tuple `(outcome, message)`. It also wrapped the comparison in `try/except TypeError` and fell back to comparing the numbers as strings. I did not keep this as written, for two reasons. First, the starter tests do `assert check_guess(50, 50) == "Win"`, which compares against a plain string, so a tuple can never pass. Second, the `except TypeError` fallback hid a real bug: the string secret should have crashed loudly, but the code silently gave wrong answers instead. In the refactored version in `logic_utils.py`, `check_guess` only returns the outcome and converts both values with `int()`. The hint text moved to a separate `get_hint_message(outcome)` function, which is easier to read and to test. I verified this by running `python -m pytest`: the three original starter tests pass unchanged, along with the new ones (20 passed).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

**How I decided a bug was really fixed:** A bug counted as fixed only when two things were true. First, a pytest test that targets that exact bug had to pass. Second, the same input from my Bug Reproduction Log had to behave correctly in the game itself. For bugs that are only about what the screen shows, like the stale "Attempts left" and the debug panel lagging, a unit test can't see the problem. For those I relied on replaying the game.

**pytest evidence:** I kept the 3 starter tests in `tests/test_game_logic.py` and added 17 new ones, one group per bug. A few examples:
- `test_too_high_hint_says_go_lower`: guess 60, secret 50 → "Too High" with the message "Go LOWER!" (backwards hints)
- `test_string_secret_is_compared_as_a_number`: `check_guess(9, "80")` → "Too Low" (string comparison bug)
- `test_negative_guess_is_rejected`: `parse_guess("-50", 1, 100)` is rejected with "Your guess must be between 1 and 100." (negative guesses)
- `test_decimal_guess_is_rejected_not_truncated`: "50.9" is rejected instead of silently becoming 50
- `test_wrong_guesses_always_cost_5_points`: "Too High" no longer adds points on even attempts

Running `python -m pytest -v` printed `20 passed`. To check that the tests really catch the bug, the two hint messages were swapped back on a temporary copy of the code. The result was `3 failed, 17 passed`, and the 3 failures were exactly the hint tests, which shows they are testing the right thing.

**Game replay evidence:** The game was replayed with Streamlit's testing tool (`AppTest`), using the inputs from my bug log:

| Input (secret) | Result after fix |
|---|---|
| Fresh game, Normal | "Attempts left: 8" (was 7) |
| 65 (89) | "Go HIGHER!", attempts left drops to 7 right away, and the debug history shows `[65]` immediately |
| 95 (89) | "Go LOWER!", attempts left 6 |
| -50 | "Your guess must be between 1 and 100.", and no attempt is used |
| 50.9 | "Please enter a whole number.", and no attempt is used |
| 8th wrong guess | "Out of attempts!" only after all 8 guesses, attempts left 0 |
| New Game | status back to playing, 8 attempts, score 0, empty history (was stuck on "Game over") |
| 42 (42) on first try | "You won!" with a score of 100 |
| Switch to Hard | range 1 to 200, new secret inside the range |

The app also started without errors using `python -m streamlit run app.py`.

**How AI helped with the tests:** Claude wrote the tests, and each one targets a single bug from my log, including my exact 65 vs 89 case. The tests helped me understand something about the code. The starter tests expected `check_guess` to return just `"Win"`, but the original code returned a tuple, so those tests could never have passed. That is why the refactor changed what `check_guess` returns. Claude also added a `pytest.ini` with `pythonpath = .`, because without it the tests in `tests/` could not import `logic_utils.py`. The AI also made a mistake I had to watch for. Its first attempt at the game replay failed because of an import path error and a 3-second timeout. That was a problem with the test harness, not with the game, and it had to be fixed before the results meant anything.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
