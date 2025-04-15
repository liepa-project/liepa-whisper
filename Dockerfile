FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04
WORKDIR /app
RUN apt-get update -y && apt-get install -y python3-pip
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r /app/requirements.txt \
      && rm -rf /root/.cache


COPY ./app/*.py  ./

#CMD ["python3", "infer.py"]

ENTRYPOINT ["./infer.py"]
