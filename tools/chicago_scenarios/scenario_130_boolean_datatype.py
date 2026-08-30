from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("boolean-datatype", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:enabled ?enabled . BIND(DATATYPE(?enabled) AS ?value) } ORDER BY ?value''', 3)

