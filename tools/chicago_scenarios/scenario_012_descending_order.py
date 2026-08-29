from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("descending-order", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value } ORDER BY DESC(?value)''', 3)
