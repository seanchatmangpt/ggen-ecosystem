from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("uppercase-name", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?name . BIND(UCASE(?name) AS ?value) } ORDER BY ?value''', 3)
