# Use a light version of Python
FROM python:3.7-slim

# Set working directory
WORKDIR /usr/app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content into the container
COPY . .

# Expose port
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
