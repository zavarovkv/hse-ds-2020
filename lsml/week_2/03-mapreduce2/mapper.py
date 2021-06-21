#!/usr/bin/env python

import sys
import time
import datetime as dt

from datetime import datetime


def get_processing_time(started_dttm, finished_dttm):
	start_time = datetime.strptime(started_dttm, '%Y-%m-%d %H:%M:%S')
	finished_time = datetime.strptime(finished_dttm, '%Y-%m-%d %H:%M:%S')

	start_time_unix = time.mktime(start_time.timetuple())
	finished_time_unix = time.mktime(finished_time.timetuple())

	return abs(finished_time_unix - start_time_unix)


def get_time_in_min(time_in_sec):
	return time_in_sec / 60


def get_employees(f_path):
	employees = {}

	with open(f_path, 'r') as reader:
		data = reader.readlines()
		for row in data:
			try:
				employee_id, manager_id, login = row.strip().split('\t')
				employees[employee_id] = [manager_id, login]
			except ValueError as e:
				continue			

	return employees


def main():
	f_employees = 'employees.txt'
	employees = get_employees(f_employees)

	for line in sys.stdin:
		try:
			contact_id, client_id, employee_id, started_dttm, finished_dttm, business_line, route_type, initiator_id = line.strip().split('\t')
		except ValueError as e:
			continue

		# check incoming requests
		if initiator_id == employee_id:
			continue

		# check at least five minutes
		time_in_sec = get_processing_time(started_dttm, finished_dttm)
		time_in_min = get_time_in_min(time_in_sec)
		if time_in_min < 5:
			continue

		# get manager login for employee
		if employee_id not in employees:
			continue

		# manager_login = employees[employee_id][1]
		manager_login = employees[employees[employee_id][0]][1]

		print "%s\t%d" % (manager_login, 1)


if __name__ == "__main__":
    main()
