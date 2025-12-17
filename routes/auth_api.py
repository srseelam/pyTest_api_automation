from core.client import APIClient
from core.env_loader import load_env
env=load_env()

class AuthAPI:
    def __init__(self): 
        self.client=APIClient()
        
    def login(self):
        payload={"username":env.USERNAME,"password":env.PASSWORD}
        return self.client.request("POST","/auth/login",json=payload)
