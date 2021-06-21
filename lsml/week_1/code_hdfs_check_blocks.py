#!/usr/bin/env python3

import requests
import json

from hdfs import Config


client = Config().get_client()
endpoint = 'http://hadoop2-10.yandex.ru:50070/webhdfs/v1/data/lsml/1-hdfs/lsml.sample'

response = requests.get(endpoint + '?op=GET_BLOCK_LOCATIONS')
data = json.loads(response.text)

failure_nodes = ['hadoop2-08.yandex.ru', 'hadoop2-12.yandex.ru', 
'hadoop2-13.yandex.ru', 'hadoop2-16.yandex.ru', 'hadoop2-17.yandex.ru', 
'hadoop2-18.yandex.ru']

blocks = []
nodes = {}
sizes = {}

for block in data['LocatedBlocks']['locatedBlocks']:
    block_id = block['block']['blockId']
    print('id: ' + str(block_id))

    block_size = block['block']['numBytes']
    print('size: ' + str(block_size))

    # save block
    blocks.append(block_id)

    # save block size to dict
    sizes[block_id] = block_size

    locations = block['locations']
    for loc in locations:
        node = loc['hostName']
        if node in failure_nodes:
            print('node (failure): ' + node)
        else:
            print('node: ' + node)

        # save nodes to dict
        if block_id not in nodes:
            nodes[block_id] = []
        nodes[block_id].append(node)

# calculate sum of all blacks sizes
total_size = 0

for block in blocks:
    total_size += sizes[block]

print('Total size: ' + str(total_size))

# calculate size of failure blocks
failure_size = 0

for block in blocks:
    cnt_nodes = len(nodes[block])
    for node in nodes[block]:
        if node in failure_nodes:
            cnt_nodes -= 1
    if cnt_nodes <= 0:
        failure_size += sizes[block]

print('Failure size: ' + str(failure_size))

answer = 100 - failure_size * 100 / total_size

print('Answer: ' + str(answer))
