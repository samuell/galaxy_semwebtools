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

if len(options.sparql_query) < 9: 
	sys.exit("Your SPARQL query is too short (printed below)!\n" + options.sparql_query)

if not re.match("^http", options.url):
	sys.exit("The URL has to start with 'http://'! Please try again!")

f = open("/home/samuel/opt/galaxy/tools/sparql_import/query.txt","w")
f.write(options.sparql_query + "\n")
f.close()

# -----------------------
# The main code
# -----------------------

def main():
	sparql_query = options.sparql_query
	sparql_query = sparql_query.replace("__oc__","{")
	sparql_query = sparql_query.replace("__cc__","}")
	sparql_query = urllib.quote_plus(sparql_query)

	url = options.url

	sparql_query_url = url + "?query=" + sparql_query

	sparql_endpoint = urllib.urlopen(sparql_query_url)
	results = sparql_endpoint.read()
	sparql_endpoint.close()

	xmldata = extract_xml( results )
	tabular = xml_to_tabular( xmldata )

	print tabular

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

def xml_to_tabular( xmldata ):
	root = et.fromstring(xmldata)
	tree = et.ElementTree(root)
	tabular = ""

	results = root.getchildren()[1]
	for result in results:
		for binding in result.getchildren():
			content = binding.getchildren()[0].text
			tabular += content + "\t"
		tabular += "\n"	
	return tabular

if __name__ == '__main__':
	main()