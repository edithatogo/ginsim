FROM python:3.11-slim@sha256:07d4824036af339fa1b6ef769cc99d9c10a141769538b52b3b597c84f7a7b535

# Set JAX platform (cpu or cuda)
ENV JAX_PLATFORMS=cpu
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    git-lfs \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

# Copy and install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e ".[dev,workflow]"

# Copy source code
COPY src/ src/
COPY scripts/ scripts/
COPY configs/ configs/
COPY Snakefile .

# Set working directory
WORKDIR /app

# Create outputs directory
RUN mkdir -p outputs

# Default command
CMD ["snakemake", "--cores", "all"]
