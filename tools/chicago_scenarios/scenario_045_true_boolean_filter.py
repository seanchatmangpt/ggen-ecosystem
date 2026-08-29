from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("true-boolean-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:enabled true ; ex:name ?value } ORDER BY ?value''', 2)
