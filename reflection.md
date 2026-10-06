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

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
