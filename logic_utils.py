def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 150  # Bug 2 fix: Hard must be a wider range than Normal (1-100)
    return 1, 100


def get_attempt_limit(difficulty: str) -> int:
    """Return the number of allowed attempts for a given difficulty."""
    limits = {
        "Easy": 11,    # Bug 3 fix: Easy should allow MORE attempts than Normal (8), not fewer
        "Normal": 8,
        "Hard": 5,
    }
    return limits.get(difficulty, 8)


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome string.

    Returns one of: "Win", "Too High", "Too Low"

    Bug 1 was here: the original code compared types incorrectly,
    so a guess of 6 vs secret 59 returned "Too High" instead of "Too Low".
    The fix: always compare as integers, check equality first.
    """
    # Equality must come first — otherwise a correct guess falls into a branch below
    if guess == secret:
        return "Win"

    # Bug 1 fix: straightforward integer comparison with correct direction
    if guess > secret:
        return "Too High"   # guess is above the secret → player must go lower

    return "Too Low"        # guess is below the secret → player must go higher
    
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")
