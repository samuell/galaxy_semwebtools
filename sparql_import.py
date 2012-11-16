#!/usr/bin/python

from optparse import OptionParser
import urllib, sys

parser = OptionParser()
parser.add_option("-q", "--sparql_query",
	help = "A SPARQL query to send to a SPARQL endpoint")
parser.add_option("-u", "--url",
	help = "The URL to the SPARQL endpoint")
(options, args) = parser.parse_args()

if not options.sparql_query:
	sys.exit("You have to specify a SPARQL query! Use the -h flag to view command line options!")
if not options.url:
	sys.exit("You have to specify an URL! Use the -h flag to view command line options!")

sparql_query = str(options.sparql_query)
url = options.url

sparql_query_url = url + "?query=" + sparql_query

# Open the URL to the SPARQL endpoint
sparql_endpoint = urllib.urlopen(sparql_query_url)
results = sparql_endpoint.read()

# Just for debugging ...
# print("SPARQL query:\n" + sparql_query)
print(results)

