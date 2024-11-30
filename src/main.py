import os
from typing import Literal, Union

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from csv_manager import CsvManager
from models.dify import (
    DifyExternalKnowledgeAPIErrorResponse,
    DifyExternalKnowledgeAPIRecord,
    DifyExternalKnowledgeAPIRequest,
    DifyExternalKnowledgeAPIResponse,
)

data_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)
address_manager = CsvManager(
    file=os.path.join(data_dir, "address.csv"), target_columns=["name"]
)

API_KEY = os.getenv("API_KEY") or "secret"

app = FastAPI()
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def validate_api_key(api_key_header: str) -> Literal[0, 1001, 1002]:
    if api_key_header == "":
        return 1001
    bearer, api_key = api_key_header.split(" ")
    if bearer != "Bearer":
        return 1001
    if api_key == API_KEY:
        return 0
    return 1002


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_msg = exc.errors()[0]["msg"] if exc.errors() else "RequestValidationError"
    return JSONResponse(
        status_code=400,
        content={
            "error_msg": error_msg,
        },
    )


@app.post("/retrieval")
async def retrieval(
    payload: Union[DifyExternalKnowledgeAPIRequest, None] = None,
    auth_header: str = Depends(api_key_header),
):
    # Validate API key
    validation_result = validate_api_key(auth_header)
    if not validation_result == 0:
        return JSONResponse(
            status_code=403,
            content=DifyExternalKnowledgeAPIErrorResponse(
                error_code=validation_result,
                error_msg="Invalid API key",
            ).model_dump_json(),
        )

    # Validate payload.
    # If payload is None, raise RequestValidationError.
    # This is a workaround for Diffy's endpoint testing.
    # The endpoint testing tool sends a request without a body.
    # In this case, the endpoint should not return DifyExternalKnowledgeAPIErrorResponse with 403 status code.
    if payload is None:
        raise RequestValidationError(errors=[{"msg": "Request body is required"}])

    knowledge_id = payload.knowledge_id
    query = payload.query
    top_k = payload.retrieval_setting.top_k
    score_threshold = payload.retrieval_setting.score_threshold

    if knowledge_id != "address":
        return JSONResponse(
            content=DifyExternalKnowledgeAPIErrorResponse(
                error_code=2001,
                error_msg="Knowledge ID not found",
            ).model_dump_json(),
        )

    # Query the CSV file
    response_array = address_manager.query(query)
    records = [
        DifyExternalKnowledgeAPIRecord(
            content=str.join(",", record.values()),
            score=1.0,
            titie=record["name"],
            metadata=None,
        )
        for record in response_array
    ]

    return DifyExternalKnowledgeAPIResponse(records=records)


if __name__ == "__main__":
    import argparse

    import uvicorn

    parser = argparse.ArgumentParser(description="Run the Uvicorn server.")
    parser.add_argument("--reload", action="store_true", help="Enable reload mode")
    args = parser.parse_args()
    uvicorn.run("main:app", reload=args.reload)
