# faster-whisper на CPU: без CUDA, образ заметно меньше, чем openai-whisper + torch[cuda].
FROM python:3.11-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "faster-whisper>=1.0.0"

COPY transcribe.py /app/transcribe.py

WORKDIR /work
ENTRYPOINT ["python", "/app/transcribe.py"]
