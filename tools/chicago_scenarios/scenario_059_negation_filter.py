from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("negation-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:enabled ?enabled ; ex:name ?value . FILTER(!?enabled) } ORDER BY ?value''', 1)

