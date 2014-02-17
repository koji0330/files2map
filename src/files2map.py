#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys, re, json, argparse
from lxml import etree

parser = argparse.ArgumentParser(
	description='Gnerate sitemap from local files.'
)
parser.add_argument(
	'files',
	metavar='html_file',
	type=file,
	nargs='+',
	help='target files'
)
parser.add_argument(
	'--config',
	dest='config',
	default='config.json',
	help='config json file (default: config.json)'
)

args = parser.parse_args()

# Load config file
f = open(args.config, "rU")
loaded = json.load(f)
f.close()

# Output header
delimiter = ''
for column in loaded['COLUMN_ORDER']:
	sys.stdout.write(delimiter)
	sys.stdout.write(column)
	delimiter = ','
print ''

# Output body
for input_file in args.files:
	html = input_file.read()
	delimiter = ''
	try:
		dom = etree.fromstring(html, etree.HTMLParser())
		for column in loaded['COLUMN_ORDER']:
			part = loaded['PARTS'][column]
			if part['type'] == 'path':
				out = input_file.name
			elif part['type'] == 'xpath':
				nodes = dom.xpath(part['value'])
				code = []
				out = ''
				for node in nodes:
					if isinstance(node, etree._ElementUnicodeResult):
						out = out + node.encode("utf-8")
					elif isinstance(node, etree._ElementStringResult):
						out = out + node.encode("utf-8")
					elif isinstance(node, etree._Element):
						out = etree.tostring(node, encoding='utf-8')
					else:
						# TODO: Fix other instance.
						print type(node)
			# Replace string, if defined.
			if 'replace' in part and out != '':
				for replacer in part['replace']:
					out = re.sub(
						replacer['before'].encode("utf-8"),
						replacer['after'].encode("utf-8"),
						out,
						flags = re.MULTILINE
					)
			if out == '':
				out = loaded['NOT_FOUND']
			sys.stdout.write(delimiter)
			sys.stdout.write(out)
			delimiter = ','
		print
	except etree.XMLSyntaxError:
		# parse error
		pass
	except:
		print "Unexpected error:", sys.exc_info()[0]
