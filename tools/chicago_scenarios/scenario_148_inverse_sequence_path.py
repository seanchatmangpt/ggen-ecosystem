from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("inverse-sequence-path", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?name ^ex:name/ex:rank ?value } ORDER BY ?value''', 3)

