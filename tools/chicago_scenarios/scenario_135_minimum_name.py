from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("minimum-name", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (MIN(?name) AS ?value) WHERE { ?s ex:name ?name } ORDER BY ?value''', 1)

