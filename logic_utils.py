def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) number range for a given difficulty.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        A tuple (low, high) representing the inclusive guessing range.
        Defaults to (1, 100) for any unrecognized difficulty string.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 150)
    """
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
    """Return the number of allowed guesses for a given difficulty.

    Easier difficulties grant more attempts so the smaller range advantage is
    balanced against the narrower search space.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        The integer attempt limit. Defaults to 8 (Normal) for any
        unrecognized or incorrectly-cased difficulty string.

    Examples:
        >>> get_attempt_limit("Easy")
        11
        >>> get_attempt_limit("Hard")
        5
    """
    # FIX (Bug 3): AI spotted Easy had only 6 attempts — fewer than Normal's 8, which is
    # backwards. Used AI agent mode to refactor the hardcoded dict out of app.py into here.
    limits = {
        "Easy": 11,
        "Normal": 8,
        "Hard": 5,
    }
    return limits.get(difficulty, 8)


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse a raw string input from the user into an integer guess.

    Handles empty input, non-numeric strings, and decimal values by
    truncating them to the nearest integer (e.g. "7.9" → 7).

    Args:
        raw: The raw string entered by the user, or None if no input exists.

    Returns:
        A three-tuple (ok, guess_int, error_message):
          - ok (bool): True if parsing succeeded.
          - guess_int (int | None): The parsed integer, or None on failure.
          - error_message (str | None): A human-readable error, or None on success.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def check_guess(guess: int, secret: int) -> str:
    """Compare a player's guess against the secret number and return the outcome.

    Args:
        guess: The integer value the player guessed.
        secret: The integer secret number chosen for this round.

    Returns:
        "Win"      if guess equals secret.
        "Too High" if guess is greater than secret.
        "Too Low"  if guess is less than secret.

    Examples:
        >>> check_guess(50, 50)
        'Win'
        >>> check_guess(60, 50)
        'Too High'
        >>> check_guess(40, 50)
        'Too Low'
    """
    # FIX (Bug 1): Original code sometimes cast secret to str, making 6 > "59" evaluate
    # as True (lexicographic). AI identified the root cause via step-by-step trace in chat
    # mode; fix was to always compare integers and check equality first.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate an updated score based on the outcome of a single guess.

    Scoring rules:
      - Win:      100 minus 10 × attempt_number, with a floor of 10 points.
      - Too High: +5 points on even attempts, -5 on odd (penalizes overshooting).
      - Too Low:  -5 points.
      - Any other outcome: score is unchanged.

    Args:
        current_score: The player's score before this guess.
        outcome: One of "Win", "Too High", or "Too Low".
        attempt_number: The 1-based index of the current attempt.

    Returns:
        The updated integer score.

    Examples:
        >>> update_score(0, "Win", 1)
        90
        >>> update_score(50, "Too Low", 3)
        45
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")
