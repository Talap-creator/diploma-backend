# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update 

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Add Poetry to the system PATH
ENV PATH="${PATH}:/root/.poetry/bin"

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Expose the port that Django will run on
EXPOSE 8000

# Run Django migrations and start the development server
CMD ["poetry", "run", "python", "manage.py", "migrate", "&&", "poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
