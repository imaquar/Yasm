FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /app/venv

RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=project.settings

RUN /app/venv/bin/python manage.py migrate

RUN /app/venv/bin/python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["/app/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]