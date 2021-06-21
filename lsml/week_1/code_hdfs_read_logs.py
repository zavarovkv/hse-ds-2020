#!/usr/bin/env python3

import json

from hdfs import Config


client = Config().get_client()
path = '/data/lsml/1-hdfs/'
client.list(path)

total_sum = 0

for i in range(0, 8):
    f = path + 'site-transactions-0' + str(i+1) + '.json'

    with client.read(f, encoding='utf-8') as reader:
        print('read file: ' + f)
        data = json.load(reader)

    for transaction in data['transactions']:
        if transaction['customerId'] == 42:
            for good in transaction['goods']:
                if good['vendorCode'] == '104':
                    sum = good['amount'] * good['pricePerUnit']
                    total_sum += sum

print(total_sum)
