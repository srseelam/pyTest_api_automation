from pydantic import BaseModel
class AuthResponse(BaseModel): token:str; id:int; username:str
