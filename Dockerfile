FROM python:3.11.6

# Copy the .kaggle directory from the host machine to the root directory of the container
COPY /Users/vambat1/.kaggle /root/.kaggle

# Copy the rest of the application files into the /app directory of the container
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Install dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Specify the command to run your application
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:5000", "app:app"]
