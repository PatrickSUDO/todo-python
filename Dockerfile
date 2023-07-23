# Base stage
FROM python:3.10-slim as base

WORKDIR /src

# Builder stage
FROM base as builder

# Install dependencies
COPY requirements/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Testing stage
FROM builder as test

# Install testing dependencies
COPY requirements/requirements-test.txt .
RUN pip install -r requirements-test.txt

# Copy tests
COPY tests /tests

CMD ["pytest", "/tests"]

# Runner stage
FROM base as runner

COPY --from=builder /usr/local /usr/local

COPY --from=builder /src .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
