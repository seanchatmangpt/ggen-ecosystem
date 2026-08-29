from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("maximum-name", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (MAX(?name) AS ?value) WHERE { ?s ex:name ?name } ORDER BY ?value''', 1)

