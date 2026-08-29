from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("same-term-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?value ex:name ?name . FILTER(sameTerm(?value, ex:a)) } ORDER BY ?value''', 1)
