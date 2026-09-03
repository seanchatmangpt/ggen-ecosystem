from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("string-integer-cast", '''PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?value WHERE { VALUES ?lexical { "42" "7" } BIND(xsd:integer(?lexical) AS ?value) } ORDER BY ?value''', 2, inline_query=True)
