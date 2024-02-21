FROM python:3.11.6

# Create a directory for the .kaggle directory in the Docker image
RUN mkdir -p /root/.kaggle

# Copy the .kaggle directory from the host machine to the Docker image
COPY ~/.kaggle/kaggle.json /root/.kaggle/

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Command to run the application
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:5000", "app:app"]
