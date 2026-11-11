FROM python:3.13-alpine@sha256:1e1f6334529d1fb26a2ef619d7cffb30a7c7d7cc1cc7338ebee283a58d1aeaca AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app/src
WORKDIR /app
RUN python -m pip uninstall --yes pip
COPY src/ /app/src/
COPY examples/ /app/examples/
COPY examples/workspaces/ /data/workspaces/
RUN mkdir -p /data/workspaces/alpha/outputs /data/workspaces/beta/outputs \
    && chown -R 10001:10001 /data/workspaces/alpha/outputs /data/workspaces/beta/outputs
USER 10001:10001

FROM base AS test
COPY tests/ /app/tests/
CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]

FROM base AS runtime
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2).read()"
CMD ["python", "-m", "ai_backend.server"]
