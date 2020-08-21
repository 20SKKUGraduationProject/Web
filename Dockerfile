FROM python:3.6

EXPOSE 8000

ADD ./backend /home/ubuntu/Web/backend

ADD ./frontend /home/ubuntu/Web/frontend

WORKDIR /home/ubuntu/Web/backend

RUN python3 -m pip install Django

RUN pip install django-jquery

RUN git clone https://github.com/django/django.git

RUN python3 -m pip install -e django/

RUN pip install requests

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"] 
