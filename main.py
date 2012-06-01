#!/usr/bin/env python

import os
import time
import commands
import shutil
import re
import random

from html_output import HtmlOutput

import email_smtp

#data region start

cases_dir = "./cases/"

details_dir = "./details/"

case_files = []

result_html = HtmlOutput()

idx = 0

note_flag = "[note]"

command_flag = "[command]"

loop_flag = "[loop]"

expect_flag = "[expect]"

flags = [note_flag, command_flag, loop_flag, expect_flag]

one_case_start_flag = note_flag

test_command = ""
test_loop = 1
expect_result = ""
failure_result_file = ""

#functions region start

def check_details_dir():
	if os.path.exists(details_dir):
		shutil.rmtree(details_dir)
	os.makedirs(details_dir)

def get_case_files_list():
	for file in os.listdir(cases_dir):
		one_case = cases_dir + file
		if os.path.isfile(one_case):
			case_files.append(one_case)

def deal_content_of_case(what, how):
	global test_command
	global test_loop
	global expect_result

	if how == note_flag:
		result_html.write_note(what)
	elif how == loop_flag:
		test_loop = what
	elif how == expect_flag:
		expect_result=what
	elif how == command_flag:
		test_command = what
	else:
		print "do not know how tot do"

def deal_test_failure(output):
	time_str = time.strftime("%Y-%m-%d-%H-%M-%S")
	random_str = str(random.random())
	file_name = details_dir + time_str + random_str
	file = open(file_name, "w")
	file.write(output)
	file.close()
	result_html.write_fail(file_name)

def do_command():
	for i in range(int(test_loop)):
		status, out = commands.getstatusoutput(test_command)
		if expect_result == "$?0":
			if status == 0:
				result_html.write_pass()
			else:
				deal_test_failure(out)
		elif expect_result == "$?!0":
			if status != 0:
				result_html.write_pass()
			else:
				deal_test_failure(out)
		else:
			out_formated = out.replace("\n", "")
			out_formated = re.sub("\t", " ", out_formated)
			out_formated = re.sub(" +", " ", out_formated)
			out_formated = re.sub("You have mail in.*", "", out_formated)
			expect_formated = expect_result 
			expect_formated = re.sub("\t", " ", expect_formated)
			expect_formated = re.sub(" +", " ", expect_formated)
			if out_formated.find(expect_formated) == -1:
				deal_test_failure(out)
			else:
				result_html.write_pass()

def do_one_case_test(one_case):
	global test_command
	global test_loop
	global expect_result

	case_lines = one_case.split("\n")

	content_begin = 0
	content = ""
	for line in case_lines:
		line = line.strip()
		if not len(line):
			continue
		for flag in flags:
			if line == flag:
				content_begin = 1
				break

		if content_begin == 1:
			if len(content):
				deal_content_of_case(content, now_flag)
			content_begin = 0
			now_flag = flag
			content = ""
			continue

		content += line

	if len(content):
		deal_content_of_case(content, now_flag)

	if len(test_command):
		do_command()

	test_command = ""
	test_loop = 1
	expect_result = ""

	time_str = time.strftime("complete this step at %Y-%m-%d %H:%M:%S")
	result_html.write_time(time_str)

def do_cases_of_file(file, idx):
	result_html.write_case_no(idx)

	print "begin test case group %d" %idx

	time_str = time.strftime("case begin running at %Y-%m-%d %H:%M:%S")
	result_html.write_time(time_str)

	f = open(file, 'r')
	begin = 0
	case = ''

	for line in f:
		line = line.strip()
		if len(line):
			if line == one_case_start_flag:
				if begin == 1:
					do_one_case_test(case)
					case = ''
				begin = 1
			case += line + '\n'

	do_one_case_test(case)

	time_str = time.strftime("case stop running at %Y-%m-%d %H:%M:%S")
	result_html.write_time(time_str)

# main flow start

check_details_dir()

get_case_files_list()

case_files.sort()
for file in case_files:
	idx += 1
	do_cases_of_file(file, idx)

result_html.close()

report_name = result_html.get_report_name()

email_smtp.mail_report(report_name)

