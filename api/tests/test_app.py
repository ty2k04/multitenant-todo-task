import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app, token_for, user_from_token

def test_health_route_is_public():
    assert app.test_client().get("/health").status_code in (200, 503)

def test_token_round_trip():
    assert user_from_token(token_for(42)) == 42

def test_tampered_token_is_rejected():
    token = token_for(42)
    tampered = token[:-3] + ("A" if token[-3] != "A" else "B") + token[-2:]
    assert user_from_token(tampered) is None

def test_todos_require_authentication():
    assert app.test_client().get("/api/todos").status_code == 401

