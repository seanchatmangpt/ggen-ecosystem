from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("limit-offset-window", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value } ORDER BY ?value LIMIT 1 OFFSET 1''', 1)

