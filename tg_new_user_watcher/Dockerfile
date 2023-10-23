FROM python:3.10-alpine

RUN apk add bash

# Создаем корневой каталог для нашего проекта в контейнере
RUN mkdir /tg_bot

# Устанавливаем рабочий каталог /django_module
WORKDIR /tg_bot

# Копируем содержимое текущего каталога в контейнер в /django_module
ADD . /tg_bot/

# Устанавливаем необходимые пакеты из requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

ENTRYPOINT ["/entrypoint"]

