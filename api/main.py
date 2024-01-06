import logging
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.settings import (
    LOG_PATH,
    LOGGER_BACKUP_COUNT,
    LOGGER_FORMAT,
    LOGGER_MAX_SIZE,
    LOGGER_MODE,
    LOGGER_NAME,
)


def _setup_logger() -> logging.Logger:
    """アプリケーションのロガーを設定し、RotatingFileHandlerを使用してログファイルのローテーションを行います。

    ログファイルは `LOG_PATH` に指定されたパスに作成され、`LOGGER_MAX_SIZE` バイトを超えると新しいファイルにローテートします。
    古いログファイルは最大 `LOGGER_BACKUP_COUNT` 個まで保持されます。ロガーとハンドラーのログレベルは `LOGGER_MODE` に設定され、
    ログメッセージのフォーマットは `LOGGER_FORMAT` の形式に従います。

    Returns:
        logging.Logger: 設定済みのロガーインスタンス。
    """
    # ログ設定
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(LOGGER_MODE)
    handler = RotatingFileHandler(filename=LOG_PATH, maxBytes=LOGGER_MAX_SIZE, backupCount=LOGGER_BACKUP_COUNT)
    handler.setLevel(LOGGER_MODE)
    handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
    logger.addHandler(handler)
    return logger


logger = _setup_logger()
app = FastAPI()
# appのルーターを設定する


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    return response


class LogResponsesMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        logger.info(f"Sent response with status code: {response.status_code}")
        return response


app.add_middleware(LogResponsesMiddleware)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.error(f"An error occurred while processing the request: {str(exc)}")
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    """アプリケーションのヘルスチェックエンドポイント。

    このエンドポイントは、アプリケーションが正常に動作しているかどうかを確認するために使用されます。
    レスポンスは、アプリケーションの状態を示すJSONオブジェクトです。

    Returns:
        dict[str, str]: アプリケーションの状態を表す辞書。例えば、{"status": "OK"}。
    """
    return {"status": "OK"}
