from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("optional-rank-fallback", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?name . OPTIONAL { ?s ex:rank ?rank } BIND(COALESCE(?rank, 0) AS ?value) } ORDER BY ?value''', 3)
