from logic_utils import check_guess

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


def test_too_high_hint_says_go_lower():
    # Regression: hints were reversed. A guess above the secret must tell the
    # player to go LOWER, not HIGHER.
    _, message = check_guess(60, 50)
    assert "LOWER" in message
    assert "HIGHER" not in message


def test_too_low_hint_says_go_higher():
    # Regression: a guess below the secret must tell the player to go HIGHER.
    _, message = check_guess(40, 50)
    assert "HIGHER" in message
    assert "LOWER" not in message


def test_secret_regenerates_when_difficulty_changes():
    # Regression: the secret was only generated once per session, so switching
    # from Normal (1-100) to Easy (1-20) could leave a secret like 70 out of range.
    from pathlib import Path
    from streamlit.testing.v1 import AppTest

    app_path = Path(__file__).resolve().parent.parent / "app.py"
    at = AppTest.from_file(str(app_path)).run()
    assert at.selectbox[0].value == "Normal"

    # Force a secret that is impossible on Easy, then switch difficulty.
    at.session_state["secret"] = 70
    at.selectbox[0].select("Easy").run()

    assert 1 <= at.session_state["secret"] <= 20
    assert at.session_state["secret_difficulty"] == "Easy"


def test_new_game_clears_game_over_state():
    # Regression: New Game only changed the secret, so status stayed "lost" and
    # the "Game over" bar (and st.stop()) persisted until the page was refreshed.
    from pathlib import Path
    from streamlit.testing.v1 import AppTest

    app_path = Path(__file__).resolve().parent.parent / "app.py"
    at = AppTest.from_file(str(app_path), default_timeout=10).run()

    # Simulate a finished game on Easy.
    at.selectbox[0].select("Easy").run()
    at.session_state["status"] = "lost"
    at.session_state["score"] = -15
    at.session_state["history"] = [3, 7, 9]
    at.run()
    assert any("Game over" in e.value for e in at.error)

    next(b for b in at.button if "New Game" in b.label).click().run()

    assert at.session_state["status"] == "playing"
    assert at.session_state["attempts"] == 0
    assert at.session_state["score"] == 0
    assert at.session_state["history"] == []
    assert 1 <= at.session_state["secret"] <= 20  # respects Easy range
    assert not any("Game over" in e.value for e in at.error)
