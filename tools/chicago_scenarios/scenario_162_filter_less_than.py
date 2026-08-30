from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("filter-less-than", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value ; ex:rank ?rank . FILTER(?rank < 3) } ORDER BY ?value''', 2)
