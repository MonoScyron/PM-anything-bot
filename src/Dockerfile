FROM python:3.9

RUN mkdir usr/bot
WORKDIR usr/bot

COPY . .

RUN pip install -r requirements.txt
CMD python main.py