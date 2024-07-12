FROM python:3.12

COPY . /app
WORKDIR /app

RUN apt update -y
RUN apt upgrade -y
RUN apt-get install -y locales
RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen 
RUN dpkg-reconfigure --frontend=noninteractive locales
RUN pip install poetry
RUN poetry install --no-root

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

