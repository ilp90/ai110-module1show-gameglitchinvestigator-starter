from logic_utils import check_guess, update_score, get_range_for_difficulty, parse_guess


# --- Starter tests (fixed to unpack the (outcome, message) tuple) ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- New tests targeting the specific bugs we fixed ---

def test_hint_message_too_high_says_go_lower():
    # Bug fixed: "Too High" hint used to say "Go HIGHER!" (backwards).
    # Now it should say "Go LOWER!" to direct the player correctly.
    _, message = check_guess(80, 50)
    assert "LOWER" in message

def test_hint_message_too_low_says_go_higher():
    # Bug fixed: "Too Low" hint used to say "Go LOWER!" (backwards).
    # Now it should say "Go HIGHER!" to direct the player correctly.
    _, message = check_guess(20, 50)
    assert "HIGHER" in message

def test_score_win_on_first_attempt():
    # Bug fixed: score formula used attempt_number + 1, deducting an extra 10 pts.
    # Winning on attempt 1 should score 90 (100 - 10*1), not 80.
    score = update_score(0, "Win", 1)
    assert score == 90

def test_score_win_on_third_attempt():
    # Winning on attempt 3 should score 70 (100 - 10*3).
    score = update_score(0, "Win", 3)
    assert score == 70

def test_hard_range_larger_than_normal():
    # Bug fixed: Hard mode returned (1, 50), easier than Normal (1, 100).
    # Hard range should be larger than Normal range.
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high

def test_correct_guess_always_wins_regardless_of_attempt_parity():
    # Bug fixed: secret was converted to string on even attempts, so a correct
    # integer guess would fail. check_guess must always return "Win" on a match.
    outcome_odd, _ = check_guess(42, 42)
    outcome_even, _ = check_guess(42, 42)
    assert outcome_odd == "Win"
    assert outcome_even == "Win"

def test_parse_guess_rejects_non_number():
    ok, val, _ = parse_guess("abc")
    assert ok is False
    assert val is None

def test_parse_guess_accepts_integer_string():
    ok, val, _ = parse_guess("37")
    assert ok is True
    assert val == 37
