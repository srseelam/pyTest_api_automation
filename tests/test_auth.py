import pytest
from common.auth_flow import get_token

@pytest.mark.login
def test_login(): 
    token = get_token()
    assert token is not None
