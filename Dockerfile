FROM python:3.11-bookworm AS builder
WORKDIR /work
RUN pip install --upgrade build
COPY . .
RUN python -m build

FROM python:3.11-slim-bookworm
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1
EXPOSE 8025
WORKDIR /opt/idems
RUN apt-get update --yes --quiet \
 && apt-get install --yes --quiet --no-install-recommends tini \
 && rm -rf /var/lib/apt/lists/*
COPY config.json config/default.json
COPY --from=builder /work/dist/*.whl .
RUN pip install *.whl
ENTRYPOINT ["tini", "--"]
CMD ["python", "-m", "aiosmtpd", "-u", "-n", "-l", "0.0.0.0:8025", "-c", "mailingester.handlers.MailServer", "config/default.json"]
