FROM python:3.11-slim
RUN apt-get update && apt-get install -y git curl nodejs npm && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
RUN mkdir -p /app/results
RUN useradd -m -u 1000 agentuser && chown -R agentuser:agentuser /app
USER agentuser
RUN git config --global user.email "agent@rift2026.ai" && \
    git config --global user.name "RIFT AI Agent" && \
    git config --global --add safe.directory '*'
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]