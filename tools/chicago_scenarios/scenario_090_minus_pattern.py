from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("minus-pattern", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value MINUS { ?s a ex:Other } } ORDER BY ?value''', 2)

