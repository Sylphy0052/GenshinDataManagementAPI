import ast
import json
import logging
from datetime import datetime
from http import HTTPStatus
from logging.handlers import RotatingFileHandler
from time import time
from typing import Any, Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.routers.user import router as user_router
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
app.include_router(user_router, tags=["ユーザ"])


@app.middleware("http")
async def log_request_response(request: Request, call_next: Callable[..., Awaitable[Response]]) -> Response:
    """HTTPリクエストとレスポンスをログに記録するミドルウェアです。
    Args:
        request (Request): 受信したHTTPリクエスト。
        call_next (Callable[..., Awaitable[Response]]): リクエストを受け取り、レスポンスを返すawaitableな結果を生成するコーラブル。
    Returns:
        Response: 後続のミドルウェアやエンドポイントハンドラーによって処理された後のHTTPレスポンス。
    Raises:
        Exception: `call_next`の実行中に例外が発生した場合にログに記録されます。
    """
    # 参考: https://blog.jicoman.info/2021/01/how-to-logging-request-and-response-body-by-fastapi/
    req_record: dict[str, Any] = dict()
    req_record["request_method"] = request.method
    req_record["request_uri"] = request.url.path
    req_record["query_params"] = str(request.query_params)
    req_record["path_params"] = str(request.path_params)
    body_dict = await request.body()
    req_record["request_body"] = str(ast.literal_eval(body_dict.decode("utf-8")) if body_dict else None)
    logger.info(json.dumps(req_record))

    time_start = time()
    response = await call_next(request)  # type: ignore
    duration = round(time() - time_start, 4)
    time_local = datetime.fromtimestamp(time_start)
    res_record: dict[str, Any] = dict()
    res_record["time_local"] = time_local.strftime("%Y/%m/%d %H:%M:%S%Z")
    res_record["duration_time"] = str(duration)
    res_record["status"] = response.status_code
    logger.info(json.dumps(res_record))
    return response


# 422エラーのハンドリング
@app.exception_handler(RequestValidationError)
async def exception_handler_422(request: Request, exc: RequestValidationError) -> JSONResponse:
    """リクエストバリデーションエラーが発生した場合に呼び出される例外ハンドラー
    Args:
        request (Request): エラーが発生したリクエストオブジェクト。
        exc (RequestValidationError): 発生したバリデーションエラーの例外インスタンス。
    Returns:
        JSONResponse: エラー詳細を含むJSONレスポンス。ステータスコードは422です。
    """
    logger.error(str(exc))
    return JSONResponse(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, content={})


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    """アプリケーションのヘルスチェックエンドポイント。

    このエンドポイントは、アプリケーションが正常に動作しているかどうかを確認するために使用されます。
    レスポンスは、アプリケーションの状態を示すJSONオブジェクトです。

    Returns:
        dict[str, str]: アプリケーションの状態を表す辞書。例えば、{"status": "OK"}。
    """
    return {"status": "OK"}
