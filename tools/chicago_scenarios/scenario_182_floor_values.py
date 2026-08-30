from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-182-floor-values", '''PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT ?value WHERE { VALUES ?n { "1.2"^^xsd:decimal "2.8"^^xsd:decimal } BIND(FLOOR(?n) AS ?value) } ORDER BY ?value''', 2, inline_query=True)
