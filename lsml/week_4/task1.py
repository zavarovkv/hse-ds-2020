#!/usr/bin/env python
# coding: utf-8

# In[148]:


import time

from datetime import datetime as dt
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import unix_timestamp



# In[149]:


spark = SparkSession.builder.master('yarn').getOrCreate()

spark = SparkSession     .builder     .appName("Python Spark Assignment")     .config("spark.some.config.option", "some-value")     .getOrCreate()
    
sc = spark.sparkContext
rdd = sc.textFile("/data/lsml/4-5-spark/flights.csv")


# In[150]:


print(rdd.count())
print(rdd.take(1))


# In[151]:


def show_head(rdd, cnt=5):
    for line in rdd.take(cnt):
        if isinstance(line, list):
            print(line)
        else:
            print([val for val in line.split(',')])


# In[152]:


show_head(rdd)


# In[153]:


rdd2 = rdd.map(
    lambda line:
        line.split(',')
).filter(
    lambda line:
        line[4] == 'SVO' and 
        line[6] == 'Arrived'
)

print(rdd2.count())
print(show_head(rdd2))


# In[154]:


rdd3 = rdd2.map(
    lambda line: 
        [line[7],
         dt.strptime(line[2] + '00', '%Y-%m-%d %H:%M:%S%z').timestamp() - \
         dt.strptime(line[8] + '00', '%Y-%m-%d %H:%M:%S%z').timestamp() >= 0,
         line[2],
         line[8]]
).filter(
    lambda line:
        line[1] is True
)

print(rdd3.count())
print(rdd3.take(5))


# In[155]:


rdd4 = rdd3.map(
    lambda line: 
        (line[0], 
         int(line[1]))
)

print(rdd4.count())
print(rdd4.take(5))


# In[156]:


rdd5 = rdd4.reduceByKey(lambda a, b: a + b).sortBy(lambda x: x[1], ascending = False)

print(rdd5.take(100))


# In[157]:


rdd6 = rdd5.map(lambda x: x[0] + ' ' + str(x[1]))


# In[158]:


for line in rdd5.collect():
    print(line)


# In[ ]:




