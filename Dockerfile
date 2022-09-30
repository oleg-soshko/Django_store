FROM python:3.10

WORKDIR /app

RUN pip install --upgrade pip

COPY ./requirements.txt /req.txt
RUN pip install -r /req.txt

COPY . /app

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
