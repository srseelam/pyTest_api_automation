from core.client import APIClient
class CartsAPI:
    def __init__(self, token=None): 
        self.client=APIClient(token)
        
    def post_add_items_to_cart(self, payload): 
        return self.client.request("POST","/carts/add",json=payload)