from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("numeric-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?value . FILTER(?value > 1) } ORDER BY ?value''', 2)
