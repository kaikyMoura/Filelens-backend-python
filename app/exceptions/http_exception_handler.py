from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "message": "An error has occurred while processing your request.",
            "error_code": exc.status_code,
        },
    )
