from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("count-star", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (COUNT(*) AS ?value) WHERE { ?s ex:name ?name } ORDER BY ?value''', 1)

