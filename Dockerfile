# Define a build argument for the Python base image version
ARG PYTHON_BASE=3.12-slim

# Use the specified Python base image as the builder stage
FROM python:$PYTHON_BASE AS builder

# Update pip and install PDM (Python Development Master)
RUN pip install -U pdm

# Set an environment variable to disable PDM update checks
ENV PDM_CHECK_UPDATE=false

# Copy necessary project files to the /project directory in the builder stage
COPY pyproject.toml pdm.lock README.md /project/

# Copy the source code to the /project/src directory in the builder stage
COPY src/ /project/src

# Set the working directory to /project
WORKDIR /project

# Install the project dependencies using PDM, with the specified options
RUN pdm install --check --prod --no-editable

# Use the specified Python base image for the final stage
FROM python:$PYTHON_BASE

# Copy the virtual environment created in the builder stage to the final stage
COPY --from=builder /project/.venv/ /project/.venv

# Add the virtual environment's bin directory to the PATH environment variable
ENV PATH="/project/.venv/bin:$PATH"

# Set the PYTHONPATH environment variable to include the source code directory
ENV PYTHONPATH="/project/src"

# Copy the source code to the /project/src directory in the final stage
COPY src /project/src

# Set the working directory to /project
WORKDIR /project

# Expose port 8080 for the application
EXPOSE 8080

# Define the default command to run the application
CMD ["python", "-u", "-m", "aitm"]
