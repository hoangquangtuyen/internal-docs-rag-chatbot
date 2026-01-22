# =========================
# Stage 1: build dependencies
# =========================
FROM public.ecr.aws/lambda/python:3.10 AS builder

WORKDIR /build

COPY requirements-lambda.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements-lambda.txt \
    -t /build/python


# =========================
# Stage 2: runtime image
# =========================
FROM public.ecr.aws/lambda/python:3.10

# Copy dependencies
COPY --from=builder /build/python ${LAMBDA_TASK_ROOT}

# Copy toàn bộ source code
COPY src/ ${LAMBDA_TASK_ROOT}/

# Lambda handler
CMD ["app.handler"]
