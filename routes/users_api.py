from utils import faker_utils
from core.client import APIClient
from models.user_model import User
class UsersAPI:
    def __init__(self, token=None): 
        self.client=APIClient(token)
        
    def post_add_user(self, payload): 
        res = self.client.request("POST", "/users/add", json=payload)
        # return User(**res.json()), res
        return res