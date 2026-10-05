# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

Many things were broken when I ran it the first time. Here are some:
1. (FIXED) Hints were backwards
2. Difficulty change doesn’t update the game settings. The number range shown in the top caption stays the same. The number of allowed attempts doesn’t change.
3. (FIXED) Difficulty change doesn’t generate a new game. The secret number stays the same after changing difficulty. The attempt count also doesn’t reset.
4. (FIXED) Easy mode has the wrong number of attempts. Easy mode is supposed to allow 6 attempts. After 4 tries, the game ended instead.
5. (FIXED) “New Game” doesn’t fully reset the game. Pressing New Game changes the secret number. However, the bottom message still says: “Game over. Start a new game to try again.”

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Change the difficulty during an active game | A new game should start with a new secret number, and the attempt count should reset for the new difficulty. | The difficulty changes, but the secret number stays the same and the attempt count does not reset. | No console error. |
| Select Easy mode and make incorrect guesses | Easy mode should allow 6 attempts before the game ends. | The game ended after 4 attempts instead of allowing 6. | No console error. |
| Lose a game, then press “New Game” | A new game should start and the “Game over. Start a new game to try again.” message should disappear. | The secret number changes, but the “Game over. Start a new game to try again.” message remains visible. | No console error. |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude from Codepath
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - Claude suggested tracking which difficulty the secret number was generated for and regenerating the secret whenever the difficulty changes. This fixed the issue where switching from Normal to Easy could leave the player with a secret number outside of Easy’s range. I verified the fix by using a pytest test. It switched from Normal to Easy and confirmed that the new secret number was within the 1–20 range. The test passed with the fix and failed when I temporarily removed it.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
  - Claude suggested a larger fix that would reset the secret, attempts, status, score, and history whenever the difficulty changed. I decided not to use it because it addressed several different bugs at once, which would make it harder to tell which change fixed each issue. Instead, I asked it to focus only on regenerating the secret when the difficulty changes. I handled the other issues separately so I could test and verify each fix individually. I verified my version with a pytest test that confirmed the secret changed to a valid Easy-mode number after switching difficulties.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I wanted a test that failed on the buggy code and passed on the fixed code. After adding a fix, I ran the test, then temporarily removed the fix to make sure the test failed, then put it back.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - test_secret_regenerates_when_difficulty_changes forces the secret to 70, switches the difficulty to Easy, and checks that the new secret is between 1 and 20. It passed with my fix and failed with assert 70 <= 20 without it. That showed the fix was what changed the behavior. I wrote a similar test for the New Game bug, and the tests pass.


- Did AI help you design or understand any tests? How?
  - Yes, I described each bug and Claude wrote the pytest cases. It also explained that these bugs are in the Streamlit script, so I needed Streamlit's AppTest and not just tests on the helper functions. It suggested the "remove the fix and see if the test fails" check too.


---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  -  Streamlit re-runs the whole script every time you click or change something, so regular variables reset each time. Anything that needs to persist, like the secret or attempts, has to go in st.session_state. Most of my bugs came from this, like the secret was only set once and New Game never reset status.
  - The app restarts from the top on every click and forgets everything, unless you saved it in a notebook that survives restarts which is basically st.session_state.



---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects? This could be a testing habit, a prompting strategy, or a way you used Git.
  - Implementing more pytests in my work, working on each bug one by one and being excruiciatingly careful over knowing that it did not touch any other part of the code while fixing 1 bug

- What is one thing you would do differently next time you work with AI on a coding task?
  - Giving it more guardrails so that I know it's not messing with other parts of the code

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - As long as a human is in the loop and overseeing everything, then it's no different than pair programming with another dev