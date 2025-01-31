FROM python:3.13-slim AS builder

# System setup
RUN apt update -y && apt install -y libffi-dev build-essential libsasl2-dev libpq-dev libjpeg-dev

WORKDIR /usr/src/app

# Copy source
COPY requirements.txt requirements.txt

# Dependencies (Python + NPM build)
RUN pip install --user -r requirements.txt --no-cache-dir

FROM node:23-slim AS node-builder

WORKDIR /usr/src/app

COPY package.json package-lock.json webpack.config.js ./
RUN npm install

COPY apps/portal/assets ./apps/portal/assets
RUN npm run build

FROM python:3.13-slim

## Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependencies
RUN apt update -y && apt install -y supervisor curl postgresql-client libjpeg-tools argon2 tzdata

WORKDIR /usr/src/app

COPY . .
COPY --from=builder /root/.local /root/.local
COPY --from=node-builder /usr/src/app/apps/portal/static ./apps/portal/static

ENV PATH=/root/.local/bin:$PATH

RUN date -I > BUILD.txt

# Configuration
COPY conf/supervisor.conf /etc/supervisord.conf
RUN chmod +x conf/entrypoint.sh

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8000/api/v1/status || exit 1

# Execution
CMD ["conf/entrypoint.sh"]
