from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("integer-datatype", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?rank . BIND(DATATYPE(?rank) AS ?value) } ORDER BY ?value''', 3)

