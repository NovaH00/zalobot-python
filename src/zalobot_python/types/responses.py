from typing import Literal, Annotated
from pydantic import BaseModel, Field

class Result(BaseModel):
    """Represents the result field in the Zalo API successful response"""

class SuccessfulResponse[T: Result](BaseModel):
    """Represents the successful response of the Zalo API"""
    ok: Literal[True] = True
    result: T = Field(description="The result when the API call is successful.")

class ErrorResponse(BaseModel):
    """Represents the error response of Zalo API"""
    ok: Literal[False] = False
    description: str = Field(description="The description of the error")
    error_code: int = Field(description="The error code")

type ZaloAPIResponse[T: Result] = Annotated[
    SuccessfulResponse[T] | ErrorResponse,
    "Represents the response of the Zalo API"
]
