#!/usr/bin/python

from optparse import OptionParser
import urllib, sys, re

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

sparql_query = str(options.sparql_query)
url = options.url

sparql_query_url = url + "?query=" + sparql_query

# Open the URL to the SPARQL endpoint
sparql_endpoint = urllib.urlopen(sparql_query_url)
results = sparql_endpoint.read()
sparql_endpoint.close()

# Just for debugging ...
# print("SPARQL query:\n" + sparql_query)
print(results)

