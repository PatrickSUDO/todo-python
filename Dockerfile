# This stage installs all the dependencies and builds the application
FROM python:3.10-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run any tests here

# Second stage: "runner" stage
# This stage copies the application from the builder stage and runs it
FROM python:3.10-slim as runner

WORKDIR /app

COPY --from=builder /app .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
