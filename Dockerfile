FROM python:3.11.6

# Create a directory for the .kaggle directory in the Docker image
RUN mkdir -p /root/.kaggle

# Create a file inside .kaggle directory
RUN echo '{"username":"vamsibatta","key":"34d8ef587a38fc9d3304498dcc8b8dd4"}' > /root/.kaggle/example_file.txt

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Command to run the application
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:5000", "app:app"]
