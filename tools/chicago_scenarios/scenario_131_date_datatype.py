from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("date-datatype", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:when ?when . BIND(DATATYPE(?when) AS ?value) } ORDER BY ?value''', 3)

