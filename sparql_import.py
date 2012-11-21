#!/usr/bin/python
# --------------------------------------------------------
# A Galaxy plugin for querying external SPARQL Endpoints
# Samuel Lampa, samuel.lampa@gmail.com
# Created: 2012-11-16
# --------------------------------------------------------

from xml.etree import ElementTree as et
from optparse import OptionParser
import urllib, sys, re

# -----------------------
# The main code
# -----------------------

def main():
	parse_options()

	# Extract command line options
	sparql_query = options.sparql_query
	sparql_query = restore_escaped_chars( sparql_query ) 

	sparql_query = urllib.quote_plus(sparql_query)
	url = options.url

	output_file = options.output_file

	# Create SPARQL query URL
	sparql_query_url = url + "?query=" + sparql_query

	# Read from SPARQL Endpoint
	sparql_endpoint = urllib.urlopen(sparql_query_url)
	results = sparql_endpoint.read()
	sparql_endpoint.close()

        # Convert to tabular format
        if "<sparql" in results:
                xmldata = extract_xml( results )
                tabular = xml_to_tabular( xmldata )
        else:
                sys.exit("No SPARQL content found in returned data!\nReturned data:\n" + "-"*80 + "\n" + results)

	# Print to file
	of = open(output_file, "w")
	of.write(tabular)
	of.close()

# -----------------------
# Helper methods
# -----------------------

def extract_xml( content ):
	'''Extract the part of the document starting with <?xml ...'''
	xmlcontent = re.search("<sparql.*", content, re.DOTALL).group(0)
	return xmlcontent

def xml_to_tabular( xmldata ):
	'''Convert SPARQL result set XML format to tabular text'''
	root = et.fromstring(xmldata)
	tree = et.ElementTree(root)
	tabular = ""

	results = root.getchildren()[1]
	for result in results:
		line_bits = [binding.getchildren()[0].text for binding in result.getchildren()]
		line = "\t".join(line_bits)
		tabular += line + "\n"	
	return tabular

def restore_escaped_chars( sparql_query ):
	sparql_query = sparql_query.replace("__oc__","{")
	sparql_query = sparql_query.replace("__ob__","[")
	sparql_query = sparql_query.replace("__cc__","}")
	sparql_query = sparql_query.replace("__cb__","]")
	sparql_query = sparql_query.replace("__cr__"," ")
	sparql_query = sparql_query.replace("__cn__"," ")
	sparql_query = sparql_query.replace("__at__","@")
	return sparql_query

def parse_options():
	parser = OptionParser()
	parser.add_option("-u", "--url",
		help = "The URL to the SPARQL endpoint")
	parser.add_option("-q", "--sparql_query",
		help = "A SPARQL query to send to a SPARQL endpoint")
	parser.add_option("-o", "--output_file",
		help = "An output file for storing the results")
	(options, args) = parser.parse_args()

	if not options.url:
		sys.exit("You have to specify an URL! Use the -h flag to view command line options!")
	if not options.sparql_query:
		sys.exit("You have to specify a SPARQL query! Use the -h flag to view command line options!")
	if not options.output_file:
		sys.exit("You have to specify an output file! Use the -h flag to view command line options!")

	if len(options.sparql_query) < 9: 
		sys.exit("Your SPARQL query is too short (printed below)!\n" + options.sparql_query)

	if not re.match("^http", options.url):
		sys.exit("The URL has to start with 'http://'! Please try again!")

if __name__ == '__main__':
	main()
