from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("lowercase-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(LCASE(STR(?name)) AS ?value) } ORDER BY ?value''', 3)
