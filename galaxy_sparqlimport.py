from optparse import OptionParser

parser = OptionParser()
parser.add_option("-q", "--sparql_query", metavar = "SPARQL_QUERY",
	help = "A SPARQL query to send to a sparql endpoint")

(options, args) = parser.parse_args()
sparql_query = str(options.sparql_query)

print("SPARQL query:\n" + sparql_query)

