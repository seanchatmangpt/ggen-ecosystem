from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-158-filter-boolean-or", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value ; ex:rank ?rank . FILTER(?rank = 1 || ?rank = 3) } ORDER BY ?value''', 2)
