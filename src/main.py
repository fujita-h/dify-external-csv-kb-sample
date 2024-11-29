from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from models.dify import (
    DifyExternalKnowledgeAPIErrorResponse,
    DifyExternalKnowledgeAPIRequest,
    DifyExternalKnowledgeAPIResponse,
)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=403,
        content=DifyExternalKnowledgeAPIErrorResponse(
            error_code=1001,
            error_msg="Error on request validation",
        ).model_dump(),
    )


@app.post("/retrieval")
async def retrieval(
    request: DifyExternalKnowledgeAPIRequest,
) -> DifyExternalKnowledgeAPIResponse:
    return DifyExternalKnowledgeAPIResponse(records=[])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
