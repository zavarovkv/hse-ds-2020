#!/usr/bin/env python

import csv
import sys
import time
import datetime as dt

from hdfs import Config
from datetime import datetime


def get_employees(f_from, f_to):
	employees = {}
	client = Config().get_client()

	with client.read(f_from, encoding='utf-8') as reader:
		with open(f_to, "w") as writer:
			data = reader.readlines()
			writer.writelines(data)


def main():
	f_employees = '/data/lsml/2-mapreduce/employees'
	f_to = 'employees.txt'
	employees = get_employees(f_employees, f_to)


if __name__ == "__main__":
    main()
