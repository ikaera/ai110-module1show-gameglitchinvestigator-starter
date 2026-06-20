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

<!-- ADDED: Filled in per Step 1 instructions -->
**Game purpose:** A number-guessing game where the player picks a difficulty (Easy / Normal / Hard), receives "Too High" or "Too Low" hints after each guess, and wins by finding the secret number within the allowed attempts.

**Bugs found:**
1. **Backwards hints (Bug 1)** — `check_guess` compared `guess` and `secret` with a type inconsistency. When `secret` was a string, Python evaluated `6 > "59"` lexicographically (comparing `"6"` vs `"5"`), flipping the result. Fix: cast both values to `int` before comparison.
2. **Hard difficulty range too narrow (Bug 2)** — "Hard" used a range of 1–50 instead of 1–150. Fix: updated `get_range_for_difficulty("Hard")` to return `(1, 150)`.
3. **Easy difficulty attempt count too low (Bug 3)** — "Easy" gave only 6 attempts (less than Normal's 8), making it paradoxically harder. Fix: set Easy → 11, Normal → 8, Hard → 5 so more attempts reward the smaller range.
4. **New Game button freezes (Bug 4)** — The handler reset `secret` and `attempts` but left `st.session_state.status = "won"`. On the next rerun Streamlit hit the win-gate and called `st.stop()`, blocking the new game. Fix: also reset `status = "playing"` and clear `history` in the handler.

## 📸 Demo Walkthrough

<!-- ADDED: Text-based walkthrough of the fixed game end-to-end -->
1. Player selects **Normal** difficulty (range 1–100, 8 attempts). The sidebar shows "Attempts remaining: 8".
2. Player enters a guess of **40**. Game returns **"Go HIGHER!"** and the attempt counter drops to 7.
3. Player enters **70**. Game returns **"Go LOWER!"** and the counter drops to 6.
4. Player enters **55**. Game returns **"Go HIGHER!"** — counter drops to 5.
5. Player enters **63**. Game returns **"Go LOWER!"** — counter drops to 4.
6. Player enters **59** — the secret number. Game displays **"You win! 🎉"** and locks the input.
7. Score updates: +1 win added to the session total shown in the sidebar.
8. Player clicks **New Game**. The banner clears, history resets, a new secret is generated, and the input unlocks — ready for another round.

## 🧪 Test Results

<!-- ADDED: Actual pytest output from Challenge 1 advanced edge-case tests -->
```
$ python -m pytest tests/test_game_logic.py -v
============================= test session starts =============================
collected 8 items

tests/test_game_logic.py::test_winning_guess                  PASSED [ 12%]
tests/test_game_logic.py::test_guess_too_high                 PASSED [ 25%]
tests/test_game_logic.py::test_guess_too_low                  PASSED [ 37%]
tests/test_game_logic.py::test_bug1_low_guess_vs_high_secret  PASSED [ 50%]
tests/test_game_logic.py::test_hard_range_exact               PASSED [ 62%]
tests/test_game_logic.py::test_hard_range_wider_than_normal   PASSED [ 75%]
tests/test_game_logic.py::test_easy_attempts_exact            PASSED [ 87%]
tests/test_game_logic.py::test_attempt_order                  PASSED [100%]

============================== 8 passed in 0.03s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
