from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("count-resources", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT (COUNT(?s) AS ?value) WHERE { ?s ex:name ?name }''', 1)
