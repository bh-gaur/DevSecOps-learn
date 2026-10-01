import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure demo-app root is in python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from main import app

@pytest.fixture(scope="module")
def client():
    """Module-level TestClient instance for testing FastAPI endpoints."""
    with TestClient(app) as test_client:
        yield test_client
