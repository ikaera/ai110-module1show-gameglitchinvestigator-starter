from logic_utils import check_guess, get_range_for_difficulty, get_attempt_limit

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_bug1_low_guess_vs_high_secret():
    # Directly reproduces Bug 1: guess 6, secret 59.
    # Before the fix the string-cast path returned "Too High" here.
    # After the fix it must return "Too Low".
    result = check_guess(6, 59)
    assert result == "Too Low"

# ── Bug 2 tests: get_range_for_difficulty() ──────────────────────────────────
# Bug 2: Hard returned (1, 50) — narrower than Normal (1, 100), which is wrong.
# Fix: Hard now returns (1, 150), a wider range than Normal.

def test_hard_range_exact():
    # Hard difficulty must use the fixed range (1, 150)
    assert get_range_for_difficulty("Hard") == (1, 150)

def test_hard_range_wider_than_normal():
    # The key rule: Hard ceiling must be higher than Normal ceiling
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high


# ── Bug 3 tests: get_attempt_limit() ─────────────────────────────────────────
# Bug 3: Easy returned 6 attempts — fewer than Normal (8), which is backwards.
# Fix: Easy = 11, so easier difficulty gives more attempts.

def test_easy_attempts_exact():
    # Easy must have exactly 11 attempts after the fix
    assert get_attempt_limit("Easy") == 11

def test_attempt_order():
    # Logical rule: easier difficulty = more attempts allowed
    # Easy (11) > Normal (8) > Hard (5)
    assert get_attempt_limit("Easy") > get_attempt_limit("Normal") > get_attempt_limit("Hard")