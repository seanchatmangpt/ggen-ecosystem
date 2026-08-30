from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-166-filter-in-set", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value ; ex:rank ?rank . FILTER(?rank IN (1,3)) } ORDER BY ?value''', 2)
