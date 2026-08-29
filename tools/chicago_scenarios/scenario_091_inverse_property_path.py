from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("inverse-property-path", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?name ^ex:name ?value } ORDER BY ?value''', 3)

