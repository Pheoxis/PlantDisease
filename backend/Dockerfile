FROM tensorflow/tensorflow:2.14.0-jupyter

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

ARG KEDRO_UID=999
ARG KEDRO_GID=0
RUN groupadd -f -g ${KEDRO_GID} kedro_group && \
useradd -d /home/kedro -s /bin/bash -g ${KEDRO_GID} -u ${KEDRO_UID} kedro

WORKDIR /home/kedro
COPY . .
RUN chown -R kedro:${KEDRO_GID} /home/kedro
USER kedro
RUN chmod -R a+w /home/kedro

EXPOSE 8888

CMD ["python3", "main.py"]
