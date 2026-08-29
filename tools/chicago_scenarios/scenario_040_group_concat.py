from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("group-concat", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (GROUP_CONCAT(STR(?name); separator=\",\") AS ?value) WHERE { ?s ex:name ?name } ORDER BY ?value''', 1)
