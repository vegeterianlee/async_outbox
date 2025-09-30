from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.common.api_response import api_response


def global_exception_handler(app: FastAPI):
    @app.exception_handler(SQLAlchemyError)
    async def handle_db_error(request: Request, exc: SQLAlchemyError):
        response = await exc.to_json()
        return JSONResponse(
            status_code=exc.status_code,
            content=api_response(
                data=response["error_message"],
                code=response["status_code"],
                success=False
            )
        )

    @app.exception_handler(HTTPException)
    async def handle_exception(request: Request, exc: HTTPException) -> JSONResponse:
        response = await exc.to_json()
        return JSONResponse(
            status_code=exc.status_code,
            content=api_response(
                data=response["error_message"],
                code=response["status_code"],
                success=False
            )
        )

    @app.exception_handler(ValueError)
    async def handle_exception(request: Request, exc: HTTPException) -> JSONResponse:
        response = await exc.to_json()
        return JSONResponse(
            status_code=exc.status_code,
            content=api_response(
                data=response["error_message"],
                code=response["status_code"],
                success=False
            )
        )

    @app.exception_handler(Exception)
    async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
        error_message = str(exc)
        return JSONResponse(
            status_code=500,
            content=api_response(
                data=error_message,
                code=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False
            )
        )