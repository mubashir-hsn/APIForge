import time
import httpx # type: ignore

from app.models.api_request import ApiRequest

from app.services.environment_service import (
    replace_variables
)


async def execute_request(
    api_request: ApiRequest
):

    start_time = time.time()

    try:

        variables = {}

        # Load environment variables
        if api_request.environment:
            variables = api_request.environment.variables

        # Replace variables in URL
        final_url = replace_variables(
            api_request.url,
            variables
        )

        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.request(
                method=api_request.method,
                url=final_url,
                headers=api_request.headers,
                params=api_request.query_params,
                json=api_request.body
            )

        end_time = time.time()

        response_time = round(
            end_time - start_time,
            3
        )

        try:
            response_body = response.json()

        except Exception:
            response_body = response.text

        return {
            "status_code": response.status_code,
            "response_time": response_time,
            "response_headers": dict(response.headers),
            "response_body": response_body,
            "error_message": None
        }

    except Exception as error:

        return {
            "status_code": None,
            "response_time": None,
            "response_headers": None,
            "response_body": None,
            "error_message": str(error)
        }