FROM pytorch/pytorch:latest
WORKDIR /
RUN apt-get update \
     && apt-get install -y \
        libgl1-mesa-glx \
        libx11-xcb1 \
     && apt-get clean all \
     && rm -r /var/lib/apt/lists/*
RUN pip install mlflow==1.20.2
RUN pip install scikit-learn
RUN pip install numpy
RUN pip install scipy
RUN pip install pandas
RUN pip install pysqlite3
RUN pip install transformers
RUN pip --no-cache-dir install torch

ENV BACKEND_URI sqlite:////mlflow/mlflow.db
ENV ARTIFACT_ROOT /mlflow/artifacts

CMD mlflow server --backend-store-uri ${BACKEND_URI} --default-artifact-root ${ARTIFACT_ROOT} --host 0.0.0.0 --port 5000
