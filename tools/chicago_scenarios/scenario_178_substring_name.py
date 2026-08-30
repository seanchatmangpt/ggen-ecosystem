from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("substring-name", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?name . BIND(SUBSTR(?name, 1, 2) AS ?value) } ORDER BY ?value''', 3)
