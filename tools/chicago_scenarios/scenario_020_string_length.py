from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("string-length", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(STRLEN(STR(?name)) AS ?value) } ORDER BY ?value''', 3)
