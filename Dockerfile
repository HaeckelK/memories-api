FROM python:3.9-slim-buster as production

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./memories /memories

RUN groupadd --gid 5000 user \
    && useradd --home-dir /home/user --create-home --uid 5000 \
        --gid 5000 --shell /bin/sh --skel /dev/null user

RUN chown user /memories

USER user

WORKDIR /memories/app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

FROM production as development
USER root
COPY requirements_dev.txt requirements_dev.txt
RUN pip3 install -r requirements_dev.txt
USER user