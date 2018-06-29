FROM python:3

ADD . /scripts
WORKDIR /scripts

RUN echo "Europe/Moscow" > /etc/timezone
RUN pip3 install --upgrade pip
RUN pip3 install pyTelegramBotAPI 
ENTRYPOINT [ "python3", "/scripts/p3imap.py"]
