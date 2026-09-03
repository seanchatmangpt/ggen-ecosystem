from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("in-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?value . FILTER(?value IN (1, 3)) } ORDER BY ?value''', 2)

