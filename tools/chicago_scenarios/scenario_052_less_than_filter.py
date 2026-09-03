from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("less-than-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?value . FILTER(?value < 3) } ORDER BY ?value''', 2)

