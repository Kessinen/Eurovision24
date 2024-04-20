FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in `requirements.txt`
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./src /app/

# Expose port 8000 and map it to our host's port 8000
EXPOSE 8000

# Run the command to start the Uvicorn server
CMD ["uvicorn", "main:app --host 0.0.0.0 --port 8000"]
