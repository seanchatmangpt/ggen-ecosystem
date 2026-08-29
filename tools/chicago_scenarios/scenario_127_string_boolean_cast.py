from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("string-boolean-cast", '''PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?value WHERE { VALUES ?lexical { "true" "false" } BIND(xsd:boolean(?lexical) AS ?value) } ORDER BY ?value''', 2, inline_query=True)
