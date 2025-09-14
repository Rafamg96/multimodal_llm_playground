FROM python:3.10-slim-bullseye

WORKDIR /demobusinessapp

# Copy project files
COPY api ./api
COPY pyproject.toml ./pyproject.toml
COPY README.md ./README.md

# Install poetry
RUN pip install --upgrade pip && pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-cache

# EXECUTE APP
EXPOSE 8000

# OPTION USING ONLY ONE WORKER OF UVICORN 
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]

