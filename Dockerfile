#FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04
FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04
WORKDIR /app
RUN apt-get update -y && apt-get install -y python3-pip
RUN pip install faster-whisper
#RUN pip install faster-whisper torch --extra-index-url https://download.pytorch.org/whl/cu124

COPY ./app/*.py  ./

#CMD ["python3", "infer.py"]

ENTRYPOINT ["./infer.py"]
