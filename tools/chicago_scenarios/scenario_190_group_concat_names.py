from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-190-group-concat-names", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT (GROUP_CONCAT(?name; separator="|") AS ?value) WHERE { ?s ex:name ?name }''', 1)
