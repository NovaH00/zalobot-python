from typing import override

class ZaloAPIError(BaseException):
    """Exception when using the Zalo API"""
    def __init__(self, error_code: int, description: str):
        self.error_code: int = error_code
        self.description: str = description
        super().__init__()

    @override
    def __str__(self):
        return f"error_code: {self.error_code}; description: {self.description}"

