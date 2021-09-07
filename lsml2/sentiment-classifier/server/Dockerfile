FROM nvidia/cuda:10.2-runtime
WORKDIR /
RUN apt-get update
RUN pip install mlflow==1.20.2
RUN pip install scikit-learn
RUN pip install numpy
RUN pip install scipy
RUN pip install pandas
RUN pip install pysqlite3
RUN pip install transformers
RUN pip --no-cache-dir install torch
