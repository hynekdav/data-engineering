FROM python:3.10-slim
LABEL authors="Hynek Davídek <hynek.davidek@gmail.com>"

# ----------------------------------------------------------------------------------------------------
# 1. System Settings
# ----------------------------------------------------------------------------------------------------
ARG PYTHONUNBUFFERED=1
ARG DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-EeuxoC", "pipefail", "-c"]

# ----------------------------------------------------------------------------------------------------
# 1. Prepare System
# ----------------------------------------------------------------------------------------------------

RUN set -eux; \
    apt-get update && apt-get install -y --no-install-recommends \
      curl \
      procps; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false

# ---------------------------------------------------------------------
# 3. Workdir
# ---------------------------------------------------------------------
ARG WORKDIR=/app
WORKDIR $WORKDIR

# ---------------------------------------------------------------------
# 4. Requirements
# ---------------------------------------------------------------------
COPY ./pyproject.toml .
RUN poetry install --no-root --no-cache --without dev --no-interaction --no-ansi

# ---------------------------------------------------------------------
# 5. App sources
# ---------------------------------------------------------------------
COPY data_prep ./data_prep
COPY visualization.py ./visualization.py
COPY entrypoint.sh ./entrypoint.sh

RUN chmod -R 111 entrypoint.sh

# ---------------------------------------------------------------------
# 6. Expose ports
# ---------------------------------------------------------------------
EXPOSE 8501

# ---------------------------------------------------------------------
# 7. Define procesess
# ---------------------------------------------------------------------
CMD ./entrypoint.sh
