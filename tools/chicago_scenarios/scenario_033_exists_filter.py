from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("exists-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?value a ex:Thing . FILTER EXISTS { ?value ex:name ?name } } ORDER BY ?value''', 2)
