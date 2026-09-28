import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from worker import config

def test_config_has_database_name():
    assert config()["database"] == "todo_app"

