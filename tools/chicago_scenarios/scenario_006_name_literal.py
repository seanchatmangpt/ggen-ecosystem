from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("name-literal", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value } ORDER BY ?value''', 3)
