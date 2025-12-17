import pytest
from utils import faker_utils
from models.user_model import User

@pytest.mark.users
def test_post_add_user(users_api):
    payload = User().build(firstName=faker_utils.fake_first_name(),
                           lastName=faker_utils.fake_last_name(),
                           email= faker_utils.fake_email(),
                           age= faker_utils.random_adult_age())
    res=users_api.post_add_user(payload); 
    assert res.status_code==201
    user = User(**res.json())
    assert user.firstName == payload["firstName"]
    assert user.lastName == payload["lastName"]
    assert user.age == payload["age"]

@pytest.mark.users    
def test_post_add_user_with_default(users_api):
    payload = User().build(firstName="Srinivasa")
    res=users_api.post_add_user(payload); 
    assert res.status_code==201
    body = res.json()
    assert body["firstName"] == payload["firstName"]
    assert body["lastName"] == payload["lastName"]
    assert body["age"] == payload["age"]

@pytest.mark.users    
def test_post_add_user_with_all_default(users_api):
    payload = User().build()
    res=users_api.post_add_user(payload); 
    assert res.status_code==201
    body = res.json()
    assert body["firstName"] == payload["firstName"]
    assert body["lastName"] == payload["lastName"]
    assert body["age"] == payload["age"]