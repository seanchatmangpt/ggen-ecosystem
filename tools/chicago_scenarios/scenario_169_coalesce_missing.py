from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("coalesce-missing", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?name . OPTIONAL { ?s ex:missing ?missing } BIND(COALESCE(?missing, ?name) AS ?value) } ORDER BY ?value''', 3)
