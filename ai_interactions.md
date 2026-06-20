# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

> "Use your AI coding assistant agentically to plan and implement a meaningful new feature, such as a 'High Score' tracker that saves your best score to a file or a 'Guess History' sidebar that visualizes how close your previous guesses were."

The agent chose to implement a **Guess History sidebar** because `st.session_state.history` was already being populated on every guess — no new data plumbing was needed, only a visualization layer.

**What did the agent do?**

1. Read `app.py` in full to understand existing session state keys (`history`, `status`, `score`, `secret`), the sidebar layout, and the difficulty range variables (`low`, `high`).
2. Planned the feature: filter `history` to numeric guesses only, compute each guess's position in the range as a 0–1 float for `st.progress()`, and reveal color-coded proximity icons (`🟢 🟡 🔴`) only after the game ends so the secret isn't accidentally leaked mid-game.
3. Edited `app.py` — added a new sidebar section at the bottom of the file with:
   - A `📊 Guess History` subheader
   - A numbered entry + progress bar for each numeric guess
   - Distance-from-secret annotation and color coding once `status` is `"won"` or `"lost"`
   - A `st.sidebar.metric` showing the running session score
4. Verified that the `history` list already excluded invalid (non-integer) inputs from the display by filtering with `isinstance(g, int)`.

**Files modified:**

| File | Change |
|------|--------|
| `app.py` | Added Guess History sidebar section (~35 lines at end of file) |
| `ai_interactions.md` | Added this Agent Workflow entry |

**What did you have to verify or fix manually?**

- Confirmed the proximity color thresholds (≤10% of range = green, ≤25% = yellow, >25% = red) made intuitive sense for all three difficulty ranges (Easy 1–20, Normal 1–100, Hard 1–150).
- Verified that `st.progress()` accepts a float 0.0–1.0, and added `max(0.0, min(1.0, ...))` clamping to guard against guesses outside the current difficulty range (e.g., a Hard-range guess reviewed on an Easy-range sidebar).
- No logic bugs were introduced — no manual corrections to the agent's code were needed.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used:**

```
Given these functions in logic_utils.py: check_guess(guess, secret),
get_range_for_difficulty(difficulty), and get_attempt_limit(difficulty),
write pytest test cases for these 9 edge cases:
[Boundary values, check_guess(1, 1) or check_guess(150, 150), off-by-one errors at range limits;
Unknown difficulty string, get_range_for_difficulty("Expert"), falls through to default — is the default sensible?;
Zero or negative guess, check_guess(0, 50) or check_guess(-5, 50), should return "Too Low" — does it?;
Guess equal to range boundary, check_guess(150, 150) on Hard, win at the exact ceiling;
Case sensitivity, get_attempt_limit("easy") vs "Easy", returns default 8, not 11 — is that correct?].
Each test should have a comment explaining why the edge case matters.
```

| Edge Case | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------------|--------------|----------------|
| Win at lower boundary (`check_guess(1, 1)`) | `test_boundary_win_lower` | ✅ Yes | 1 is the floor of every range; equality must still register as a win, not misfire as "Too Low" |
| Win at Hard upper boundary (`check_guess(150, 150)`) | `test_boundary_win_upper_hard` | ✅ Yes | 150 is the Hard ceiling; a correct guess there must not be treated as "Too High" |
| Too High just above lower boundary (`check_guess(2, 1)`) | `test_boundary_too_high_just_above` | ✅ Yes | Verifies the "Too High" branch works right at the edge, not just mid-range |
| Too Low just below upper boundary (`check_guess(149, 150)`) | `test_boundary_too_low_just_below` | ✅ Yes | Verifies the "Too Low" branch works at the Hard ceiling without off-by-one error |
| Zero guess (`check_guess(0, 50)`) | `test_zero_guess` | ✅ Yes | 0 is below every valid range; must return "Too Low" without crashing |
| Negative guess (`check_guess(-5, 50)`) | `test_negative_guess` | ✅ Yes | Negative numbers are out-of-range inputs that should be handled gracefully |
| Unknown difficulty range (`get_range_for_difficulty("Expert")`) | `test_unknown_difficulty_range` | ✅ Yes | Confirms the fallback `(1, 100)` is returned instead of an error for undefined difficulties |
| Unknown difficulty attempts (`get_attempt_limit("Expert")`) | `test_unknown_difficulty_attempts` | ✅ Yes | Confirms the fallback `8` is returned instead of `None` or a crash |
| Case-sensitive lookup (`get_attempt_limit("easy")`) | `test_case_sensitivity_attempts` | ✅ Yes | Documents that lowercase bypasses the dict and hits the default — a deliberate behavior to be aware of |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
