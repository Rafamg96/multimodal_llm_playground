FROM python:3.10-slim-bullseye

WORKDIR /demobusinessapp

# Copy project files
COPY api ./api
COPY pyproject.toml ./pyproject.toml
COPY README.md ./README.md


# Install ffmpeg to avoid error about audio processing
RUN apt update -y && apt install -y ffmpeg

#####################################################
######### Install dependencies using uv ##############
#####################################################
# Install uv
RUN pip install --upgrade pip && pip install uv

# Configure uv env variables
ENV UV_NO_PROGRESS=1 \
    UV_CACHE_DIR=/tmp/uv_cache


# Install dependencies using uv with private registry authentication
RUN . ~/.bashrc && \
    uv pip install --system --index-strategy unsafe-best-match -e .[dev,test] && \
    rm -rf $UV_CACHE_DIR

EXPOSE 8000

# OPTION USING ONLY ONE WORKER OF UVICORN 
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]

