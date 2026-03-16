def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIXME: Hard mode originally returned (1, 50) — smaller than Normal, making it easier.
    # FIX: Claude Code identified the range was backwards; changed to (1, 1000) so Hard is
    #      genuinely harder than Normal.
    if difficulty == "Hard":
        return 1, 1000
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
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


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIXME: Original hints were backwards — "Too High" said "Go HIGHER!" and
    #        "Too Low" said "Go LOWER!", actively pointing the player the wrong way.
    # FIX: Claude Code flagged the swapped emoji and text; corrected so each hint
    #      directs the player toward the secret number.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIXME: Original formula was `100 - 10 * (attempt_number + 1)`, which
        #        deducted an extra 10 points on every win (winning on attempt 1 gave
        #        80 instead of 90).
        # FIX: Claude Code spotted the off-by-one; removed the `+ 1`.
        points = 100 - 10 * attempt_number
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
