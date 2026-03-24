"""HTTP utility module for making async requests to the Zalo API."""

from typing import Literal, Any

import httpx

from ..types import ZaloAPIResponse, Result, SuccessfulResponse, ErrorResponse

async def fetch[T: Result](
    url: str,
    *,
    result_schema: type[T],
    method: Literal["GET", "POST"] = "GET",
    body: dict[str, Any] | None = None,
    timeout: int = 30,
) -> ZaloAPIResponse[T]:
    """Utility function to fetch data from the Zalo API asynchronously.
    
    This function handles HTTP communication with the Zalo Bot API, automatically
    parsing responses into the appropriate schema types.
    
    Args:
        url: The API endpoint URL to request.
        result_schema: The Pydantic model class to validate the result against.
        method: HTTP method to use ("GET" or "POST"). Defaults to "GET".
        body: Optional JSON body for POST requests.
        timeout: Request timeout in seconds. Defaults to 30.
    
    Returns:
        ZaloAPIResponse[T]: Either a SuccessfulResponse with validated result
                           or an ErrorResponse with error details.
    
    Example:
        ```python
        response = await fetch(
            "https://bot-api.zaloplatforms.com/botTOKEN/getMe",
            result_schema=BotInfo
        )
        if isinstance(response, SuccessfulResponse):
            bot_info = response.result
        ```
    """
    async with httpx.AsyncClient(timeout=timeout) as client:

        if method == "GET":
            response = await client.get(url)

        elif method == "POST":
            response = await client.post(url, json=body)

        response_json = response.json()

        if response_json.get("ok"):
            return SuccessfulResponse(
                ok=True,
                result=result_schema.model_validate(response_json.get("result"))
            )

        return ErrorResponse(
            ok=False,
            description=response_json.get("description"),
            error_code=response_json.get("error_code")
        )
