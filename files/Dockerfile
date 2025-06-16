FROM debian:bullseye-slim

RUN apt update && apt install -y python3 certbot python3-dnspython && apt-get clean


COPY ./namesiloapi.py /root/namesiloapi.py
COPY ./authenticator.py /root/authenticator.py
COPY ./cleanup.py /root/cleanup.py
COPY ./certbot-run.py /root/certbot-run.py

WORKDIR /root
CMD ["./certbot-run.py"]
