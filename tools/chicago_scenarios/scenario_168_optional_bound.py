from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-168-optional-bound", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value . OPTIONAL { ?s ex:missing ?optional } FILTER(!BOUND(?optional)) } ORDER BY ?value''', 3)
