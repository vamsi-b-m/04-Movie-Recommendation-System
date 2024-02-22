
FROM python:3.11.6

# Copy the application code into the container
COPY . /app

# Create a directory for the .kaggle directory in the Docker image
RUN mkdir -p /root/.kaggle

# Create a file inside .kaggle directory with Kaggle API credentials
RUN echo '{"username":"vamsibatta","key":"34d8ef587a38fc9d3304498dcc8b8dd4"}' > /root/.kaggle/kaggle.json

# Change permissions of kaggle.json file to ensure it's only readable by the owner
RUN chmod 600 /root/.kaggle/kaggle.json

# Set the working directory
WORKDIR /app

EXPOSE 80 8080 5000

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Command to run the application
CMD ["python3", "app.py"]
