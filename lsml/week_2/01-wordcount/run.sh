#!/usr/bin/env bash

OUT_DIR="streaming_wc_result"
NUM_REDUCERS=8

hadoop fs -rm -r -skipTrash $OUT_DIR*

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
	-D mapreduce.job.reduces=${NUM_REDUCERS} \
	-D mapred.job.name="my_wordcount_example" \
	-files mapper.py, reducer.py \
	-combiner reducer.py \
	-mapper ./mapper.py \
	-reducer ./reducer.py \
	-input /data/lsml/2-mapreduce/contacts_part \
	-output $OUT_DIR

for num in seq 0 $(($NUM_REDUCERS - 1))
do
	hdfs dfs -cat ${OUT_DIR}/part-0000${num} | sort -k2rn | head
done
