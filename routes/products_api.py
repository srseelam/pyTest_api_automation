from core.client import APIClient
class ProductsAPI:
    def __init__(self, token=None): 
        self.client=APIClient(token)
        
    def get_all_products(self): 
        return self.client.request("GET","/products")
    
    def get_product(self,id): 
        return self.client.request("GET",f"/products/{id}")
    
    def search_products(self,searchTerm): 
        return self.client.request("GET",f"/products/search?q={searchTerm}")
