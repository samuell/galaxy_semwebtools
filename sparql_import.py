#!/usr/bin/python
# --------------------------------------------------------
# A Galaxy plugin for querying external SPARQL Endpoints
# Samuel Lampa, samuel.lampa@gmail.com
# Created: 2012-11-16
# --------------------------------------------------------

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

	results = extract_xml( results )

	# Just for debugging ...
	# print("SPARQL query:\n" + sparql_query)
	print(results)

	# Open the URL to the SPARQL endpoint
	resultdoc = pyquery(results)

# -----------------------
# Helper methods
# -----------------------

def extract_xml( content ):
	xmlcontent = re.search("<\?xml.*", content, re.DOTALL).group(0)
	return xmlcontent

if __name__ == '__main__':
	main()