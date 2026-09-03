from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("string-decimal-cast", '''PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?value WHERE { VALUES ?lexical { "12.5" "7.25" } BIND(xsd:decimal(?lexical) AS ?value) } ORDER BY ?value''', 2, inline_query=True)
