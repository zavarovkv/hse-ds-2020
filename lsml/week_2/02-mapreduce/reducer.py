#!/usr/bin/env python

import sys


def read_stdin(line):
	employee_id, start_time, finished_time, processing_time, is_incoming, is_telephony = line.strip().split('\t')
	return employee_id, int(start_time), int(finished_time), int(processing_time), int(is_incoming), int(is_telephony)	


def get_time_in_days(time_in_sec):
	return time_in_sec / 60 / 60 / 24 


def main():
	current_employee_id = None

	incoming_time = 0
	outcoming_time = 0

	incoming_cnt = 0
	outcoming_cnt = 0

	worked_min = None
	worked_max = None

	for line in sys.stdin:
		try:
			employee_id, start_time, finished_time, processing_time, is_incoming, is_telephony = read_stdin(line)
		except ValueError as e:
			continue

		if current_employee_id != employee_id:

			if current_employee_id:
				if incoming_cnt == 0: incoming_cnt = 1
				if outcoming_cnt == 0: outcoming_cnt = 1

				avg_incoming = incoming_time / incoming_cnt
				avg_outcoming = outcoming_time / outcoming_cnt

				if worked_max == None: continue
				if worked_min == None: continue

				if get_time_in_days(worked_max - worked_min) > 180:
					print "%s\t%d\t%d" % (current_employee_id, avg_incoming, avg_outcoming)

			incoming_time = 0
			outcoming_time = 0

			incoming_cnt = 0
			outcoming_cnt = 0

			worked_min = None
			worked_max = None

			current_employee_id = employee_id

		if bool(is_telephony):
			if bool(is_incoming):
				incoming_cnt += 1
				incoming_time += processing_time
			else:
				outcoming_cnt += 1
				outcoming_time += processing_time

		if worked_min:
			if start_time < worked_min:
				worked_min = start_time
		else:
			worked_min = start_time

		if worked_max:
			if finished_time > worked_max:
				worked_max = finished_time
		else:
			worked_max = finished_time

	if current_employee_id:
		if incoming_cnt == 0: incoming_cnt = 1
		if outcoming_cnt == 0: outcoming_cnt = 1

		avg_incoming = incoming_time / incoming_cnt
		avg_outcoming = outcoming_time / outcoming_cnt

		if worked_max == None: return
		if worked_min == None: return

		if get_time_in_days(worked_max - worked_min) > 180:
			print "%s\t%d\t%d" % (current_employee_id, avg_incoming, avg_outcoming)


if __name__ == "__main__":
	main()
