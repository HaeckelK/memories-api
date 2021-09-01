FROM python:3.9-slim-buster as production

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./memories /memories

WORKDIR /memories/app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

FROM production as development
COPY requirements_dev.txt requirements_dev.txt
RUN pip3 install -r requirements_dev.txt
