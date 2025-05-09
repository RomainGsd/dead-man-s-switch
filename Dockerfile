FROM python:3.12

RUN mkdir -p /opt/dms/ && \
 useradd -ms /bin/bash dms && \
 chown -R dms /opt/dms

USER dms

COPY --chown=dms requirements.txt /opt/dms/
RUN pip3 install --no-cache-dir --user -r /opt/dms/requirements.txt

COPY --chown=dms . /opt/dms
WORKDIR /opt/dms

RUN export PATH="$PATH":/home/dms/.local/bin

LABEL maintainer="RomainGsd" \
        version="1.0.0"

CMD ["python3", "src/main.py"]
