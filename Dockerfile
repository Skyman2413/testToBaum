FROM python:3.11

RUN mkdir /test_app

WORKDIR /test_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#WORKDIR src

#CMD ["python3", "main.py"]