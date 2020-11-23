FROM python:3.9
WORKDIR /app

ADD ./requirements.txt  /app
RUN pip install -r requirements.txt

ADD . /app
CMD python send_email_web.py
