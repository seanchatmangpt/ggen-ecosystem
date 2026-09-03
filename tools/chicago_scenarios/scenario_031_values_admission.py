from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("values-admission", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { VALUES ?value { ex:a ex:c } ?value ?p ?o } ORDER BY ?value''', 2, inline_query=True)
