from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("not-exists-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?value a ex:Thing . FILTER NOT EXISTS { ?value ex:missing ?x } } ORDER BY ?value''', 2)
