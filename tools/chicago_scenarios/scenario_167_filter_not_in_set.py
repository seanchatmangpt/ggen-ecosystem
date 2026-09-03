from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-167-filter-not-in-set", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value ; ex:rank ?rank . FILTER(?rank NOT IN (2,4)) } ORDER BY ?value''', 2)
