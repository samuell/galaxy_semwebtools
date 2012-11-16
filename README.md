# Semantic Web Tools for Galaxy #

## SPARQL Import tool ##
This toolkit currently just contains a tool that enables to specify an URL to a SPARQL endpoint, and a SPARQL query, and to save the returned data in tabular format, for further processing in Galaxy's tools.

## Installation ##

1. Create a folder "semweb_tools" under [galaxy_root]/tools/ and add these files.
2. Add the following section right under the starting &lt;toolbox&gt; tag in [galaxy_root]/tool_conf.xml:

````
    <section name="Semantic Web Tools" id="semweb_tools">
        <tool file="semweb_tools/sparql_import.xml" />
    </section>
````

## Change log ##

* 2012-11-16: Now works properly (at least for my simple test case)!
* 2012-11-16: Created today, still under heavy development!
