import requests
import pytest
from core.logger import logger
from core.env_loader import load_env
env = load_env()

class APIClient:
    def __init__(self, token=None):
        self.base = env.BASE_URL; self.token = token
    def _headers(self):
        h={"Content-Type":"application/json"};
        if self.token: h["Authorization"] = f"Bearer {self.token}";
        return h
    
    # def request(self, method, endpoint, **kwargs):
    #     url=f"{self.base}{endpoint}"
    #     logger.info(f"REQUEST: {method} {url}")
    #     logger.info(f"HEADERS: {self._headers()}")
    #     logger.info(f"PAYLOAD: {kwargs.get('json')}")
    #     res=requests.request(method,url,headers=self._headers(),**kwargs)
    #     logger.info(f"RESPONSE CODE: {res.status_code}")
    #     logger.info(f"RESPONSE BODY: {res.text}")
    #     return res
    
    def request(self, method, endpoint, **kwargs):
        url=f"{self.base}{endpoint}"
         # Merge headers correctly
        headers = self._headers()
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs
        )
        try:
            node = pytest.current_test_node
            node._request_data = {
                "method": method,
                "url": url,
                "headers": headers,
                "payload": kwargs.get("json"),
            }
            node._response_data = {
                "status_code": response.status_code,
                "body": response.text,
            }
        except Exception as e:
            print("Logging failed:", e)

        return response