from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("group-concat-distinct", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (GROUP_CONCAT(DISTINCT STR(?name); separator="|") AS ?value) WHERE { ?s ex:name ?name } ORDER BY ?value''', 1)

