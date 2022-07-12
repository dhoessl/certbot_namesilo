FROM debian:bullseye-slim

RUN sudo apt update && sudo apt install -y python3 python3-pip && apt-get clean

RUN pip3 install xmltodict certbot

COPY ./namesiloapi.py /root/namesiloapi.py
COPY ./authenticator.py /root/authenticator.py
COPY ./cleanup.py /root/cleanup.py
COPY ./certbot-run.py /root/certbot-run.py

WORKDIR /root
CMD ["./certbot-run.py"]
