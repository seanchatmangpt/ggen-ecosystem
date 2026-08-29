from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("select-expression-alias", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (STR(?name) AS ?value) WHERE { ?s ex:name ?name } ORDER BY ?value''', 3)

