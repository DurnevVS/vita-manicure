FROM python:3.12

COPY . /app
WORKDIR /app

RUN apt-get update -y \
  && apt-get install locales -y --no-install-recommends \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
  && dpkg-reconfigure --frontend=noninteractive locales \
  && pip --no-cache-dir install -r requirements.txt 
# && python manage.py migrate

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

