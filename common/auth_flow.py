from routes.auth_api import AuthAPI

def get_token():
    res=AuthAPI().login(); assert res.status_code==200
    return res.json().get("accessToken")

