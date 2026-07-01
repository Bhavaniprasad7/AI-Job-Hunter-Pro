FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY README.md .
COPY config config
COPY src src

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .

EXPOSE 8501

CMD ["streamlit", "run", "src/ai_job_hunter_pro/ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
