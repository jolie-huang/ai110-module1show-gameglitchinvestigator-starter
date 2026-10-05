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

- Game Glitch Investigator is a number-guessing game built with Streamlit. You pick a difficulty (Easy, Normal or Hard), guess the secret number, and get "Go higher" or "Go lower" hints. The starter code was AI-generated and contained intentional bugs. The goal of the project was to find them, fix them, and write tests to prove the fixes work.
- Some bugs that I found were:
   - Reversed hints: a guess that was too high told the player to go higher, and a guess that was too low told them to go lower.
   - Secret didn't change with difficulty: the secret was only generated once per session, so switching from Normal to Easy could leave a secret like 70 while the range was 1–20.
   - New Game didn't clear the game-over state: it only changed the secret, so the "Game over" bar stayed on screen until the page was refreshed. It also ignored the difficulty range, and didn't reset the score or history.
   - Hardcoded range text: the message always said "between 1 and 100", whatever the difficulty.
   - Attempts didn't reset when difficulty changed.
- The fixes I applied were:
   - Hints: corrected the messages in check_guess. Tests check that "Too High" says go lower and "Too Low" says go higher.
   - Secret: the app now remembers which difficulty the secret was generated for (secret_difficulty) and regenerates the secret when the difficulty changes. A pytest test using Streamlit's AppTest forces a secret of 70, switches to Easy, and checks the new secret is between 1 and 20.
   - New Game: it now resets the status, score and history, and picks the secret from the current difficulty's range. A test simulates a lost game, clicks New Game, and checks the "Game over" bar is gone.
   - Refactor: I moved the game logic out of app.py into logic_utils.py, so it can be tested on its own.
   (Each fix is marked with a #FIX comment in the code. I checked each test by removing the fix to confirm the test failed.)

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User selects Normal difficulty (range 1–100); the secret is, say, 55
2. User enters a guess of 40, and the game shows "📈 Go HIGHER!" (Too Low)
3. User enters a guess of 70, and the game shows "📉 Go LOWER!" (Too High)
4. User switches to Easy, and the game generates a new secret between 1 and 20
5. User clicks New Game, and the "Game over" message clears, the score and history reset, and a new secret is picked
6. User enters the correct guess, and the game shows balloons, "You won!" and the final score, then stops accepting guesses until New Game


**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
========================================================================== test session starts ===========================================================================
platform darwin -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/jolie/Downloads/codepathai110/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.15.1
collected 7 items                                                                                                                                                        

tests/test_game_logic.py .......                                                                                                                                   [100%]

=========================================================================== 7 passed in 0.93s ============================================================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
