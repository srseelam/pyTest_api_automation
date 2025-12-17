from pydantic import BaseModel, Field

class User(BaseModel):
    firstName: str = Field(default="John")
    lastName: str = Field(default="Doe")
    email: str = Field(default="john.doe@example.com")
    age: int = Field(default=25)

    def build(self, **overrides):
        """Return a JSON payload with overrides applied."""
        allowed_fields = self.model_dump().keys()
        for key in overrides:
            if key not in allowed_fields:
                raise ValueError(f"Invalid field passed: {key}")
        data = self.model_dump()
        data.update(overrides)
        return data