from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("numeric-type-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:amount ?value . FILTER(isNumeric(?value)) } ORDER BY ?value''', 3)

