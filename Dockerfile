FROM python:3.11.6

COPY . /app

# Create a directory for the .kaggle directory in the Docker image
RUN mkdir -p /root/.kaggle

# Create a file inside .kaggle directory
RUN echo {"username":$KAGGLE_USERNAME,"key":$KAGGLE_KEY} > /root/.kaggle/kaggle.json

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]