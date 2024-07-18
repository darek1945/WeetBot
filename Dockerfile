# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the rest of the application code
COPY ./src .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the bot
CMD ["python", "weetBot.py"]