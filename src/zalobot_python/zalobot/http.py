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
    """Ultility function to fetch the data from the Zalo API asynchronously"""
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
