# ベースイメージの指定
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコピー
COPY . .

# Streamlitの設定
EXPOSE 8501
ENV STREAMLIT_SERVER_PORT 8501

# アプリケーションの起動
CMD ["streamlit", "run", "app.py"]
