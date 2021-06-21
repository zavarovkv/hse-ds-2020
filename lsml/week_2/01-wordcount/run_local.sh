#!/usr/bin/env bash

OUT_DIR="out"
NUM_REDUCERS=4
CONFIG="--config /opt/cloudera/parcels/CDH/etc/hadoop/conf.empty"

hdfs ${CONFIG} dfs -rm -r -skipTrash ${OUT_DIR}

yarn ${CONFIG} jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
	-D mapreduce.job.name="Wordcount local" \
	-D mapreduce.job.reduces=$NUM_REDUCERS \
	-files mapper.py, reducer.py \
	-mapper ./mapper.py \
	-reducer ./reducer.py \
	-input in \
	-output ${OUT_DIR}

for num in seq 0 $(($NUM_REDUCERS - 1))
do
	hdfs ${CONFIG} dfs -cat ${OUT_DIR}/part-0000$num | head
done
