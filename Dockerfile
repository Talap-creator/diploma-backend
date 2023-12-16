# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock /app/

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Add Poetry bin directory to the PATH
ENV PATH="${PATH}:/root/.local/bin"

# Install project dependencies using Poetry
RUN poetry install --no-interaction --no-ansi

# Copy the rest of the application code to the container
COPY . /app

# Expose the port that Django will run on
EXPOSE 8000

# Run Django migrations and start the development server
CMD ["poetry", "run", "python", "manage.py", "migrate", "&&", "poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

RUN echo "Current directory: $(pwd)" && \
    echo "Installed packages: $(poetry show -v)"