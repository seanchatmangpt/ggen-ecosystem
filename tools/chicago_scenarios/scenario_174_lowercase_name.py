from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-174-lowercase-name", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?name . BIND(LCASE(?name) AS ?value) } ORDER BY ?value''', 3)
