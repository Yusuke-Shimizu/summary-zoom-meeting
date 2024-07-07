# ベースイメージの指定
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコピー
COPY *.py .

# Streamlitの設定
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# アプリケーションの起動
ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]