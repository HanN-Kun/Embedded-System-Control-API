from pydantic import BaseModel

class LocalizedMessageResponse(BaseModel):
    key: str
    language: str
    message: str