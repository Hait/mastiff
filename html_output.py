#!/usr/bin/env python

import os
import time

class HtmlOutput():
	"""produce the html report"""

	out_dir = "./out/"
	html_title = "Automatic Test"

	def __init__(self):
		if not os.path.exists(self.out_dir):
			os.makedirs(self.out_dir)
		self.file_name = time.strftime("%Y-%m-%d-%H-%M-%S")
		self.file_name = self.out_dir + self.file_name + ".htm"
		self.html_file = open(self.file_name, "w")
		self.html_file.write("<html>\n<head>\n<title>")
		self.html_file.write(self.html_title)
		self.html_file.write("</title>\n</head>\n<body>\n")

	def close(self):
		self.html_file.write("</body>\n</html>\n")
		self.html_file.close()

	def get_report_name(self):
		return self.file_name

	def write_case_no(self, no):
		self.html_file.write("<br><br><p><bold><h1>Test Case Group No. ")
		no_str = "%d" %no
		self.html_file.write(no_str)
		self.html_file.write("</h1></bold></p>\n")

	def write_time(self, str):
		self.html_file.write("<p>")
		self.html_file.write(str)
		self.html_file.write("</p>\n")

	def write_pass(self):
		self.html_file.write("<p><bold><font color=green><h3>test\
 result - PASS</h3></font></bold></p>\n")

	def write_fail(self, line):
		self.html_file.write("<p><font color=red><bold><h3>test\
 result - FAILED</font></h3></bold></p>\n")
		self.html_file.write("<p>failure details file ")
		self.html_file.write(line)
		self.html_file.write("</p>\n")

	def write_note(self, line):
		self.html_file.write("<p><bold><h2>Case description\
</h2></bold></p>\n")
		self.html_file.write("<p>")
		self.html_file.write(line)
		self.html_file.write("</p>\n")


