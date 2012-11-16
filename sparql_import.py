#!/usr/bin/python
# --------------------------------------------------------
# A Galaxy plugin for querying external SPARQL Endpoints
# Samuel Lampa, samuel.lampa@gmail.com
# Created: 2012-11-16
# --------------------------------------------------------

from xml.etree import ElementTree as et
from optparse import OptionParser
from pyquery import PyQuery as pyquery
import urllib, sys, re

# -----------------------
# Option parsing
# -----------------------

parser = OptionParser()
parser.add_option("-u", "--url",
	help = "The URL to the SPARQL endpoint")
parser.add_option("-q", "--sparql_query",
	help = "A SPARQL query to send to a SPARQL endpoint")
(options, args) = parser.parse_args()

if not options.url:
	sys.exit("You have to specify an URL! Use the -h flag to view command line options!")
if not options.sparql_query:
	sys.exit("You have to specify a SPARQL query! Use the -h flag to view command line options!")

if not re.match("^http", options.url):
	sys.exit("The URL has to start with 'http://'! Please try again!")

# -----------------------
# The main code
# -----------------------

def main():
	sparql_query = str(options.sparql_query)
	url = options.url

	sparql_query_url = url + "?query=" + sparql_query

	sparql_endpoint = urllib.urlopen(sparql_query_url)
	results = sparql_endpoint.read()
	sparql_endpoint.close()

	xmldata = extract_xml( results )

	#print("XMLDATA:\n" + xmldata)
	#print("-"*80)

	root = et.fromstring(xmldata)
	tree = et.ElementTree(root)
	outline = ""

	results = root.getchildren()[1]
	for result in results:
		for binding in result.getchildren():
			content = binding.getchildren()[0].text
			outline += content + "\t"
		outline += "\n"

	print outline

	#for result in results.findall("result"):
	#	print result.tag, result.attrib

	# Just for debugging ...
	# print("SPARQL query:\n" + sparql_query)
	# print(xmldata)

# -----------------------
# Helper methods
# -----------------------

def extract_xml( content ):
	xmlcontent = re.search("<\?xml.*", content, re.DOTALL).group(0)
	return xmlcontent

if __name__ == '__main__':
	main()