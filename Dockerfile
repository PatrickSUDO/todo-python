# This stage installs all the dependencies and builds the application
FROM python:3.10-slim as builder

WORKDIR /src

# Install dependencies
COPY requirements/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Second stage: "runner" stage
# This stage copies the application from the builder stage and runs it
FROM python:3.10-slim as runner

COPY --from=builder /usr/local /usr/local
WORKDIR /src

COPY --from=builder /src .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
