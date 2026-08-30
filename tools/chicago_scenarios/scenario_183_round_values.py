from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-183-round-values", '''PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT ?value WHERE { VALUES ?n { "1.4"^^xsd:decimal "2.6"^^xsd:decimal } BIND(ROUND(?n) AS ?value) } ORDER BY ?value''', 2, inline_query=True)
