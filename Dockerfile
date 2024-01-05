# 使用するベースイメージの指定
FROM python:3.10.6

# # appディレクトリのコピー
# COPY ./app /app
# # Poetryの設定ファイルのコピー
# COPY ./pyproject.toml /app/pyproject.toml
# COPY ./poetry.lock /app/poetry.lock

# 環境変数の設定
ENV PATH $PATH:/root/.local/bin

# 作業場所の変更
WORKDIR /app

# Poetryのインストール(共有)
RUN curl -sSL https://install.python-poetry.org | python -

# # Poetryのインストール
# RUN curl -sSL https://install.python-poetry.org | python - && \
#     poetry install

# CMD poetry run uvicorn api.main:app --host 0.0.0.0 --port 80
