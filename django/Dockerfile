FROM python
LABEL maintainer="Tomo <example@example.com>"

ENV PYTHONUNBUFFERED 1
RUN mkdir /code /static /project && \
    apt-get update && \
    apt-get -y install libjpeg-dev && \
    pip install --upgrade pip
WORKDIR /code
ADD ./code/requirements.txt /code/
RUN pip install -r requirements.txt
ADD ./code/ /code/
