from pydantic import BaseModel, Field
from typing import List

class LexRequest(BaseModel):
    code: str = Field(..., description="Java source")
    keep_comments: bool = Field(False, description="Return comments as tokens")

class TokenOut(BaseModel):
    type: str
    lexeme: str
    line: int
    column: int

class LexResponse(BaseModel):
    tokens: List[TokenOut]
