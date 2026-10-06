FROM python:3.11-slim
WORKDIR /app
COPY requirements-lock.txt .
RUN pip install --no-cache-dir -r requirements-lock.txt
COPY server.py ./
COPY docs ./docs
ENV PYTHONUNBUFFERED=1
USER 65534:65534
ENTRYPOINT ["python", "-u", "server.py"]
