def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX (Bug 2): AI identified Hard returned 1-50, narrower than Normal's 1-100.
    # Collaborated with AI chat mode to confirm the correct range should be 1-150.
    if difficulty == "Hard":
        return 1, 150
    return 1, 100


def get_attempt_limit(difficulty: str) -> int:
    """Return the number of allowed attempts for a given difficulty."""
    # FIX (Bug 3): AI spotted Easy had only 6 attempts — fewer than Normal's 8, which is
    # backwards. Used AI agent mode to refactor the hardcoded dict out of app.py into here.
    limits = {
        "Easy": 11,
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
    """
    # FIX (Bug 1): Original code sometimes cast secret to str, making 6 > "59" evaluate
    # as True (lexicographic). AI identified the root cause via step-by-step trace in chat
    # mode; fix was to always compare integers and check equality first.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"
    
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")
