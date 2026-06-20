# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input Used                                                       | Expected Behavior                           | Actual Behavior                                                                                                    | Console Error / Output |
| ---------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| 6 (secret #: 59)                                                 | "Go HIGHER!" hint                           | "Go LOWER!" hint shown                                                                                             | none                   |
| Change difficulty from normal (range 1-100, attempts: 8) to hard | Range should increase and attempts decrease | instead Range decreases, attempts decrease is normal (range 1-50, attempts: 5)                                     | none                   |
| Change difficulty from normal (range 1-100, attempts: 8) to easy | Range should decrease and attempts increase | Range decreases but attempts also decrease from 8 to 6 (range 1-20, attempts: 6)                                   | none                   |
| push New Game                                                    | start new game                              | "You already won. Start a new game to play again"- persists, history does not clear up and new game does not start | none                   |

---

## 2. How did you use AI as a teammate?

I used **Claude Code** (Anthropic's AI coding assistant, running inside VS Code) throughout this project in both chat mode and agent mode. I used it to trace buggy logic, propose fixes, generate tests, and review my own understanding of Streamlit session state.

---

### ✅ Correct AI Suggestion — Bug 1: Backwards hint direction

**What the AI suggested:**
When I described the symptom — guessing 6 against a secret of 59 showed "Go LOWER!" instead of "Go HIGHER!" — the AI stepped through the original `check_guess` function and identified that the secret number was occasionally being cast to a string before comparison. In Python, `6 > "59"` evaluates lexicographically (comparing `"6"` vs `"5"` as characters), which made the function return `"Too High"` when it should have returned `"Too Low"`. The AI suggested always comparing both values as integers and checking equality first before the greater-than/less-than branches.

**Was it correct?**
Yes, completely correct.

**How I verified it:**
I read the original `check_guess` code in [logic_utils.py](logic_utils.py) and confirmed there was a type inconsistency in how `secret` was handled. I then updated the function to:

```python
if guess == secret:
    return "Win"
if guess > secret:
    return "Too High"
return "Too Low"
```

I ran the game manually, entered 6 with the Developer Debug Info panel open (which shows the actual secret), and confirmed that when my guess was lower than the secret, the hint correctly read "Go HIGHER!" I also read the commit message from `ebd7a21` which documents this fix.

---

### ❌ Incorrect / Misleading AI Suggestion — Bug 3: Easy difficulty attempt count

**What the AI suggested:**
When I asked the AI why "Easy" mode only gave 6 attempts while "Normal" gave 8, the AI initially suggested this might be intentional — perhaps "Easy" was meant to mean a smaller number range (1–20) combined with fewer attempts to keep the game short. It framed this as a possible design choice rather than a bug, and suggested I leave the attempt counts as-is and just fix the number range.

**Was it correct?**
No, this was misleading. The suggestion confused the game's design intent. A difficulty level called "Easy" should give the player *more* attempts to make it more forgiving, not fewer. The number range being smaller (1–20 vs 1–100) already makes it easier — reducing attempts on top of that was clearly a bug, not a feature.

**How I verified it:**
I compared all three difficulty settings side-by-side in [logic_utils.py:14-23](logic_utils.py#L14-L23) after the fix:

```python
limits = {
    "Easy": 11,
    "Normal": 8,
    "Hard": 5,
}
```

With 11 attempts on Easy (small range), 8 on Normal (medium range), and 5 on Hard (large range of 1–150), the progression now makes sense — more attempts compensate for a harder range. I tested each difficulty in the running Streamlit app and confirmed the sidebar correctly displayed the updated attempt counts. The AI's original framing would have left a genuine usability bug unfixed.

---

## 3. Debugging and testing your fixes

### How I decided a bug was really fixed

I used a two-step check for every bug: first I verified the fix by reading the updated code and reasoning through the logic myself, then I confirmed the behavior either by running the Streamlit app manually or by running the pytest suite. A bug was only "done" when both steps agreed — code that looked right but still failed in the game was not fixed.

---

### Manual verification (Bug 4 — New Game freezes)

For the "New Game" button bug, I tested it manually in the running Streamlit app because session-state resets cannot easily be unit-tested in isolation. Steps:

1. Started a game, guessed until I won (status → `"won"`).
2. Confirmed the "You already won" banner appeared and the input was blocked.
3. Clicked **New Game**.
4. Before the fix: the banner persisted and the input stayed blocked. After adding `st.session_state.status = "playing"` and `st.session_state.history = []` to the handler in [app.py:105-111](app.py#L105-L111), the game fully reset: the banner was gone, the history was cleared, and a new secret was generated.

This manual test was the only practical way to catch state that survived a `st.rerun()`.

---

### pytest suite (Bugs 1, 2, 3)

I asked Claude Code to generate targeted pytest cases in [tests/test_game_logic.py](tests/test_game_logic.py) that directly reproduced each bug's root cause. The suite covers 8 cases:

| Test | What it checks |
|---|---|
| `test_bug1_low_guess_vs_high_secret` | `check_guess(6, 59)` returns `"Too Low"` — the exact input that was backwards before the fix |
| `test_hard_range_exact` | `get_range_for_difficulty("Hard")` returns `(1, 150)` |
| `test_hard_range_wider_than_normal` | Hard ceiling > Normal ceiling (structural rule, not just a magic number) |
| `test_easy_attempts_exact` | `get_attempt_limit("Easy")` returns `11` |
| `test_attempt_order` | `Easy > Normal > Hard` attempt counts hold simultaneously |
| `test_winning_guess`, `test_guess_too_high`, `test_guess_too_low` | Baseline `check_guess` coverage |

Running the suite after all fixes:

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

All 8 passed, confirming that `check_guess`, `get_range_for_difficulty`, and `get_attempt_limit` all behave correctly after the fixes.

---

### How AI helped design the tests

I prompted Claude Code: *"Generate a pytest case that specifically targets the bug in `check_guess` — guess 6, secret 59 should return 'Too Low'."* The AI produced `test_bug1_low_guess_vs_high_secret` with a comment explaining that this exact input triggered the original string-cast path. It also suggested writing a *structural* test (`test_hard_range_wider_than_normal`) instead of just a magic-number assertion — meaning the test encodes the design rule ("Hard must be wider than Normal") rather than just the current value `150`. That distinction was helpful because a future refactor could change `150` to `200` and the structural test would still be correct without modification.

---

## 4. What did you learn about Streamlit and state?

Imagine every time you click a button or type something on a webpage, the entire Python script runs again from top to bottom — that is what Streamlit does. It calls this a **rerun**. There is no "remember what happened last time" built into the script itself, so if you just wrote `score = 0` at the top, it would reset to zero on every single click.

**Session state** is the solution. It is a dictionary (`st.session_state`) that Streamlit keeps alive between reruns for as long as your browser tab is open. Anything you store there — the secret number, the current attempt count, whether the game is won or lost — survives the rerun. The pattern you see everywhere in `app.py` is:

```python
if "score" not in st.session_state:
    st.session_state.score = 0
```

That `if` guard means "only initialize this the very first time; leave it alone on every rerun after that."

Bug 4 in this project was a direct consequence of misunderstanding this. The original New Game handler only reset `attempts` and `secret`, but left `st.session_state.status = "won"` untouched. On the very next rerun (triggered by `st.rerun()`), the script hit the gate check at line 113, saw `status != "playing"`, and called `st.stop()` — freezing the game before the player could do anything. The fix was to also reset `status` back to `"playing"` and clear `history`. Session state is powerful precisely because it persists, but that means every piece of state you set during a game must be explicitly cleared when you want a fresh start.

---

## 5. Looking ahead: your developer habits

### Habit I want to reuse: reproduce-first, fix-second testing

Before touching any code, I forced myself to write down the exact input that caused the wrong output (e.g., "guess 6, secret 59 → shows 'Go LOWER!'"). That reproduction step made the AI's help dramatically more focused — instead of asking "why are hints wrong?", I could ask "why does `check_guess(6, 59)` return 'Too High'?" and get a precise root-cause answer instead of generic guesses. I will carry this habit into every future lab: before asking an AI or writing a fix, record the minimal input that breaks the thing. It also made writing the pytest cases trivial, because the reproduction step is almost identical to a test case.

### One thing I would do differently

I would verify AI suggestions against the code *before* accepting them, not after. In Bug 3, I nearly skipped fixing the attempt counts because the AI framed them as a design choice. I only caught the mistake by manually comparing all three difficulty settings side by side. Next time I will treat every AI framing of "this might be intentional" as a flag to go double-check the design intent myself — AI does not know what the original author meant, so it defaults to charity.

### How this project changed my thinking about AI-generated code

I came in assuming AI-generated code was either obviously broken or obviously fine. What I found instead is that it can be subtly wrong in ways that look reasonable on the surface — the hint logic worked correctly most of the time, which is exactly what makes that kind of bug dangerous. I now treat AI-generated code the way I would treat code from a junior teammate: worth reading carefully, not rubber-stamping.
