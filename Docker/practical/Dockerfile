FROM python:3.12-slim
LABEL maintainer = 'surajbhavake@gmail.com'
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# COPY requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m appuser
USER appuser
EXPOSE 8000
# HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    # CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
