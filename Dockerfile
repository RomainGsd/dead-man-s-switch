FROM python:3.9-alpine

RUN mkdir -p /opt/dms/
RUN adduser -D dms
RUN chown -R dms /opt/dms
USER dms

COPY --chown=dms requirements.txt /opt/dms/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --user -r /opt/dms/requirements.txt
RUN export PATH=$PATH:/home/dms/.local/bin

COPY --chown=dms . /opt/dms
WORKDIR /opt/dms

LABEL maintainer="RomainGsd" \
        version="1.0"

CMD ["python3", "src/main.py"]