from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("limit-window", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value } ORDER BY ?value LIMIT 2''', 2)
