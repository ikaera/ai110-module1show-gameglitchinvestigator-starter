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


# ── Edge Case Tests ───────────────────────────────────────────────────────────

# Edge Case 1: Win at the lower boundary of any range (off-by-one guard)
def test_boundary_win_lower():
    # 1 is the smallest valid guess across all difficulties; equality must still register as a win
    result = check_guess(1, 1)
    assert result == "Win"

# Edge Case 2: Win at the upper boundary of the Hard range
def test_boundary_win_upper_hard():
    # 150 is the Hard ceiling; a correct guess there must be "Win", not "Too High"
    result = check_guess(150, 150)
    assert result == "Win"

# Edge Case 3: Guess exactly one above the lower boundary (Too High path at boundary)
def test_boundary_too_high_just_above():
    # guess=2, secret=1 — verifies "Too High" works right at the lower edge, not just mid-range
    result = check_guess(2, 1)
    assert result == "Too High"

# Edge Case 4: Guess exactly one below the upper Hard boundary (Too Low path at boundary)
def test_boundary_too_low_just_below():
    # guess=149, secret=150 — verifies "Too Low" works right at the upper Hard ceiling
    result = check_guess(149, 150)
    assert result == "Too Low"

# Edge Case 5: Zero as a guess (lowest possible numeric input)
def test_zero_guess():
    # 0 is below every valid range; it must return "Too Low", not crash or misfire
    result = check_guess(0, 50)
    assert result == "Too Low"

# Edge Case 6: Negative guess
def test_negative_guess():
    # Negative numbers are outside the game's range entirely; must still return "Too Low" gracefully
    result = check_guess(-5, 50)
    assert result == "Too Low"

# Edge Case 7: Unknown difficulty string falls through to a sensible default range
def test_unknown_difficulty_range():
    # "Expert" is not a defined difficulty; the fallback (1, 100) should be returned, not an error
    result = get_range_for_difficulty("Expert")
    assert result == (1, 100)

# Edge Case 8: Unknown difficulty string falls through to a sensible default attempt limit
def test_unknown_difficulty_attempts():
    # "Expert" is not defined; fallback should be 8 (Normal), not crash or return None
    result = get_attempt_limit("Expert")
    assert result == 8

# Edge Case 9: Case-sensitive difficulty lookup — lowercase "easy" is not the same as "Easy"
def test_case_sensitivity_attempts():
    # get_attempt_limit("easy") hits the dict miss path and returns the default 8, not 11.
    # This test documents that behavior so a future case-insensitive fix is a deliberate choice.
    result = get_attempt_limit("easy")
    assert result == 8