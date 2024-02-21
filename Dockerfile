FROM python:3.11.6

COPY . /app

# Create a directory for the .kaggle directory in the Docker image
RUN mkdir -p ~/.kaggle

# Create a file inside .kaggle directory
RUN echo {"username":"vamsibatta","key":"34d8ef587a38fc9d3304498dcc8b8dd4"} > ~/.kaggle/kaggle.json

RUN chmod 600 ~/.kaggle/kaggle.json

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]