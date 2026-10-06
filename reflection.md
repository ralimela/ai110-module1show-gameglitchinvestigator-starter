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

I used Claude Code in VS Code (agent mode). I pasted in my notes from section 1 about all the bugs I saw and asked it to find what was causing them. After that I asked it to move the logic into logic_utils.py, fix the bugs, and write tests.

**One suggestion that was correct:** I thought the hints were just backwards, but Claude found there were actually two problems. The "Go HIGHER" and "Go LOWER" messages were swapped. Also, on every second guess, the code turned the secret number into text (a string). When you compare text instead of numbers, "9" counts as bigger than "80" because it only looks at the first character. Since attempts started at 1, my very first guess was always compared as text, which is why 65 told me to go lower when the answer was 89. This made sense because it explained every wrong hint I got, not just some of them. To check it, there is now a test that uses my exact case (guess 65, secret 89) and expects "Go HIGHER", and it passes. When we replayed the game, 65 now says "Go HIGHER" like it should.

**One suggestion I did not accept as written:** The original check_guess function (which was also written by AI) returned two things at once, the result and the message. It also had a try/except that quietly switched to comparing text whenever something went wrong. We didn't keep it that way. The starter tests check `check_guess(50, 50) == "Win"`, so they expect just the result, and returning two things meant those tests could never pass. The try/except was also hiding the real bug. Instead of crashing and showing an error, it just gave wrong hints, which made it really hard to figure out what was going on. Now check_guess only returns "Win", "Too High" or "Too Low" and always compares numbers. The message comes from a separate small function. I checked this by running pytest, and the 3 original starter tests pass without changing them.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I counted a bug as fixed when there was a test for it that passed, and when the same input from my bug log worked correctly in the game. Some bugs, like "Attempts left" not updating or the debug section showing my guess late, are about what shows up on the screen, and a normal test can't really catch that. For those I had to go by how the game actually behaved.

We kept the 3 starter tests and added 17 more, so 20 in total. Some of the ones I think are most useful:
- Guess 60 with a secret of 50 should say "Go LOWER"
- Comparing 9 to "80" should be "Too Low" (this checks the text comparison bug)
- A guess of -50 should be rejected with "Your guess must be between 1 and 100."
- 50.9 should be rejected instead of turning into 50
- A wrong guess should always cost 5 points

Running `python -m pytest -v` showed **20 passed**. One thing I found interesting: to make sure the tests actually work, we put the hint bug back on purpose in a copy of the code. Exactly the 3 hint tests failed. That showed me a test is only useful if it can actually fail when the bug is there.

We also replayed the game using my inputs from the bug log:

| What I did | What happens now |
|---|---|
| Started a new game on Normal | Shows 8 attempts left (was 7) |
| Guessed 65 (secret 89) | Says "Go HIGHER", attempts go down to 7 right away, and the guess shows in the debug section right away |
| Guessed 95 (secret 89) | Says "Go LOWER" |
| Guessed -50 | Error message, and it doesn't use up an attempt |
| Guessed 50.9 | Asks for a whole number, and it doesn't use up an attempt |
| Used all 8 guesses | Only then says "Out of attempts!" |
| Clicked New Game | Starts a new game with 8 attempts and score 0 (before, it was stuck on "Game over") |
| Guessed right on the first try | "You won!" with a score of 100 |
| Switched to Hard | Range is now 1 to 200 |

The AI helped a lot with the tests. It wrote them, and each one is tied to a bug I found, including my 65 vs 89 case. It also explained why the starter tests could never pass with the old code. One more thing I learned: the tests couldn't even find logic_utils.py at first, so Claude added a small pytest.ini file to fix that. It also didn't get everything right the first time. Its first try at replaying the game failed because of a setup problem, and it had to fix that before the results meant anything. That reminded me to check what the AI says instead of just believing it.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time you click a button or type something, Streamlit runs your whole Python file again from the top. That's called a rerun. So any normal variable gets reset every time. If you pick the secret number with random in a normal variable, you get a new secret on every click. Session state is like a notebook that Streamlit keeps between reruns, so things like the secret, score and attempts don't get lost. The biggest thing I learned is that the order of the code really matters. The "Attempts left" box and the debug section were drawn before the code that handled my guess, so they always showed old information from the turn before. I thought the counter was broken, but it was really just showing things in the wrong order. Also, session state only changes if you change it yourself. The New Game button reset the attempts but forgot to reset the "lost" status, so the game still thought it was over.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

A habit I want to keep is writing down each bug with what I typed, what I expected and what actually happened, and then turning it into a test. My 65 vs 89 bug turned into a real test, so if that bug ever comes back, I'll know right away. I also want to keep checking that my tests can fail, not just that they pass.

Next time, I would work on one bug at a time instead of giving the AI everything at once. The assignment said to use a separate chat for each bug, and I see why now. When the AI changes a lot of files at once, it's harder to read through and understand every change. Some changes also happened that I didn't ask for, like making Hard go up to 200, and I just went with them. I would also play the game myself after each fix instead of only trusting the automated checks.

This project showed me that AI code can look clean and say it's "production-ready" and still be full of bugs. From now on I'll treat AI code as a first draft that I need to test and understand, not as a finished answer.
