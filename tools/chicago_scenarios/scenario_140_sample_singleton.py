from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("sample-singleton", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (SAMPLE(?name) AS ?value) WHERE { ?s ex:name ?name } GROUP BY ?name ORDER BY ?value''', 3)

