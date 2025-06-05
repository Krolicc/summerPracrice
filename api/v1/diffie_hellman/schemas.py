from pydantic import BaseModel


class PublicKeyUpload(BaseModel):
    public_key: str
