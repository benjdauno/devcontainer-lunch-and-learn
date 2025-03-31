# Use the official Python image as a base
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel

# Create a workspace directory
WORKDIR /workspace

# Install common dev tools
RUN pip install pylint flake8

# Set up a non-root user for the container
ARG USERNAME=devcontainer
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && chown -R $USERNAME:$USERNAME /workspace

USER $USERNAME

# Default command
CMD ["python"]
