"""Exception classes for the Zalo API.

This module defines custom exceptions raised when interacting with the Zalo Bot API.
"""

from typing import override

class ZaloAPIError(BaseException):
    """Exception when using the Zalo API.
    
    This exception is raised when the Zalo API returns an error response.
    It contains both the error code and description for debugging.
    
    Example:
        ```python
        try:
            await bot.sendMessage("invalid_chat", "Hello")
        except ZaloAPIError as e:
            print(f"Error {e.error_code}: {e.description}")
        ```
    """
    
    def __init__(self, error_code: int, description: str):
        """Initialize a ZaloAPIError instance.
        
        Args:
            error_code: The numeric error code from the API.
            description: Human-readable description of the error.
        """
        self.error_code: int = error_code
        self.description: str = description
        super().__init__()

    @override
    def __str__(self):
        return f"error_code: {self.error_code}; description: {self.description}"

