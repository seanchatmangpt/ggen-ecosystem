from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("decimal-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:amount ?value . FILTER(?value >= 7.25) } ORDER BY ?value''', 2)
