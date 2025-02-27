FROM python:3.12-slim-bookworm

WORKDIR /app
COPY src .
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN addgroup --system --gid 1001 appgroup
RUN adduser --system --uid 1001 --ingroup appgroup appuser

RUN chown -R appuser:appgroup /app
RUN chmod -R 774 /app

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload", "--log-level", "debug"]
