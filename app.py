import random
import streamlit as st
from logic_utils import get_range_for_difficulty, get_attempt_limit, check_guess


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)
attempt_limit = get_attempt_limit(difficulty)  # Bug 3 fix: Easy=11, Normal=8, Hard=5

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)
# FIX (Bug 4): AI explained that the original handler only reset attempts/secret, leaving
# status="won"/"lost" and a stale history. The gate check at line ~114 then called st.stop()
# immediately, freezing the game. Collaborated with AI chat mode to identify all three missing
# resets: status → "playing", history → [], and secret range tied to difficulty.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)
        secret = st.session_state.secret

        outcome = check_guess(guess_int, secret)

        if show_hint:
            messages = {"Win": "🎉 Correct!", "Too High": "📉 Go LOWER!", "Too Low": "📈 Go HIGHER!"}
            st.warning(messages.get(outcome, ""))

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")

# ── Guess History Sidebar ─────────────────────────────────────────────────────
st.sidebar.divider()
st.sidebar.subheader("📊 Guess History")

numeric_history = [g for g in st.session_state.history if isinstance(g, int)]

if not numeric_history:
    st.sidebar.caption("No guesses yet.")
else:
    game_over = st.session_state.status in ("won", "lost")
    secret = st.session_state.secret

    for i, guess in enumerate(numeric_history, start=1):
        distance = abs(guess - secret)
        range_span = high - low

        # Position in range as 0.0–1.0 for the progress bar
        position = max(0.0, min(1.0, (guess - low) / range_span))

        if game_over:
            # Color-code by proximity: green ≤10%, yellow ≤25%, red >25%
            proximity_pct = distance / range_span
            if proximity_pct <= 0.10:
                icon = "🟢"
            elif proximity_pct <= 0.25:
                icon = "🟡"
            else:
                icon = "🔴"
            label = f"#{i}: **{guess}** {icon} (off by {distance})"
        else:
            label = f"#{i}: **{guess}**"

        st.sidebar.markdown(label)
        st.sidebar.progress(position)

    if game_over:
        st.sidebar.caption(f"Secret was **{secret}**.")

st.sidebar.divider()
st.sidebar.metric("Session Score", st.session_state.score)
