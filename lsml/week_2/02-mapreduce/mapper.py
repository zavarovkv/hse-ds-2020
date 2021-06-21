#!/usr/bin/env python

import sys
import time
import datetime as dt

from datetime import datetime


def get_unix_time(dttm):
	t = datetime.strptime(dttm, '%Y-%m-%d %H:%M:%S')
	return time.mktime(t.timetuple())


def main():
	for line in sys.stdin:
		try:
			_, client_id, employee_id, started_dttm, finished_dttm, business_line, route_type, initiator_id = line.strip().split('\t')
		except ValueError as e:
			continue

		# only CREDIT CARD business segment.
		if business_line.lower() != 'CREDIT CARD'.lower():
			continue

		# time to unix time
		start_time = get_unix_time(started_dttm)
		finished_time = get_unix_time(finished_dttm)

		# get processing time
		processing_time = abs(finished_time - start_time)

		# incoming or outcoming
		is_incoming = True
		if initiator_id == employee_id:
			is_incoming = False

		# telephony or not
		is_telephony = True
		if route_type.lower() != 'TELEPHONY'.lower():
			is_telephony = False

		print "%s\t%d\t%d\t%d\t%d\t%d" % (employee_id, start_time, finished_time, processing_time, is_incoming, is_telephony)


if __name__ == "__main__":
	main()
