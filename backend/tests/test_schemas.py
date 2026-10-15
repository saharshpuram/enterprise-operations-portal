import pytest
from pydantic import ValidationError
from app.schemas import StatusUpdate

def test_valid_status():
    assert StatusUpdate(status="RESOLVED").status == "RESOLVED"

def test_invalid_status():
    with pytest.raises(ValidationError):
        StatusUpdate(status="UNKNOWN")
