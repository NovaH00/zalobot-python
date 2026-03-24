"""Response models for the Zalo API.

This module defines the base response types returned by the Zalo Bot API,
including successful responses, error responses, and type aliases.
"""

from typing import Literal, Annotated
from pydantic import BaseModel, Field

class Result(BaseModel):
    """Represents the result field in the Zalo API successful response.
    
    This is a base class for all result models in the API.
    """

class SuccessfulResponse[T: Result](BaseModel):
    """Represents the successful response of the Zalo API.
    
    Attributes:
        ok: Always True for successful responses.
        result: The result data specific to the API endpoint called.
    """
    ok: Literal[True] = True
    result: T = Field(description="The result when the API call is successful.")

class ErrorResponse(BaseModel):
    """Represents the error response of Zalo API.
    
    Attributes:
        ok: Always False for error responses.
        description: Human-readable description of the error.
        error_code: Numeric error code for programmatic handling.
    """
    ok: Literal[False] = False
    description: str = Field(description="The description of the error")
    error_code: int = Field(description="The error code")

type ZaloAPIResponse[T: Result] = Annotated[
    SuccessfulResponse[T] | ErrorResponse,
    "Represents the response of the Zalo API"
]
