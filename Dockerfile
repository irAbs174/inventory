FROM python:3.10.4
WORKDIR /black
COPY . .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
EXPOSE 8282
CMD python manage.py runserver 0.0.0.0:8282