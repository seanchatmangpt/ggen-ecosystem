from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-157-filter-boolean-and", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value ; ex:enabled true ; ex:rank ?rank . FILTER(?rank >= 1 && ?rank <= 3) } ORDER BY ?value''', 2)
