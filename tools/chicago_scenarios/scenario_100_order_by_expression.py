from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("order-by-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (?name AS ?value) WHERE { ?s ex:name ?name ; ex:rank ?rank } ORDER BY DESC(?rank)''', 3)

