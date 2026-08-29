from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("boolean-disjunction", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:enabled ?enabled ; ex:name ?value . FILTER(?enabled = true || ?value = "Beta") } ORDER BY ?value''', 3)

