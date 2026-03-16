# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

Initially when i started playing the game it suggested me to enter any number between 1-100 as a guess. The hint suggested me to go higher for each guess and even if I entered 100 it suggested me to go even higher and that's when I realised the hints are not accurate (the actual number was 53). When I put the same number and keep guessing, the hints that are given were inconsistent, once it says higher and once it says lower!

Also when I click on new game, the game doesn't start a new game and gets stuck without allowing me to guess.

The other bug that I noticed was that even when I had one attempt left, the game ended saying I was out of attempts and shows me the answer. Since I have an attempt left, I tried to enter the correct answer but it said the game was over.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used GPT-5.2 for most parts of my project 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Copilot suggested that my “higher/lower” hints were wrong because the comparison/hint logic needed to consistently treat the secret as a number and return the correct direction (too high → “LOWER”, too low → “HIGHER”). I implemented that in logic_utils.py and wired the app to use the shared logic. I verified it by running the game (streamlit run app.py) and checking the hints matched my guesses, and by running python -m pytest and seeing all tests pass (including a regression test checking the message contains “LOWER”).

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
At one point, the AI/test idea assumed check_guess() would return just a string like "Too High" and suggested asserting check_guess(60, 50) == "Too High". That was misleading because my function actually returns a tuple (outcome, message), so that assertion would be testing the wrong thing. I verified this by looking at the return value in logic_utils.py and then fixing the tests in test_game_logic.py to unpack outcome, message; after that change, pytest passed.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed only if I could reproduce the original problem, apply the change, and then consistently not reproduce it anymore. For the hint bug, I verified it manually by running `streamlit run app.py` and trying guesses that were clearly above or below the secret to confirm the hint direction stayed correct and didn’t flip between turns. I also verified it with pytest by running `python -m pytest` after adding a small regression test that checks a too-high guess returns the “Too High” outcome and the hint message contains “LOWER”. This showed me my logic was behaving the same way every time and that the test would catch the bug if it came back. AI helped by suggesting what a focused regression test should assert (outcome + key word in the hint), and it also helped me realize I needed to align the tests with the function’s actual return shape.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
