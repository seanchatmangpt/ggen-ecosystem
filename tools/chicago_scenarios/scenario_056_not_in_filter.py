from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("not-in-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?value . FILTER(?value NOT IN (2)) } ORDER BY ?value''', 2)

