FROM python:3.10

WORKDIR /app
COPY ./ /app
COPY requirements.txt /app
RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]
