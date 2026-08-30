from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("sample-name", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT (SAMPLE(?name) AS ?value) WHERE { ?s ex:name ?name }''', 1)
