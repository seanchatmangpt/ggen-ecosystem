from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-160-filter-equal", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value ; ex:rank ?rank . FILTER(?rank = 2) }''', 1)
