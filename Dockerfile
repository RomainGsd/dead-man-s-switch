FROM python:3.9-alpine


#Use layer caching
COPY requirements.txt /
RUN python3 -m pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "src/main.py"]