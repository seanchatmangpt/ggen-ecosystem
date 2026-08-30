from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-171-concat-names", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?name . BIND(CONCAT("item-", ?name) AS ?value) } ORDER BY ?value''', 3)
