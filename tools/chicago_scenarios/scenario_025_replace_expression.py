from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("replace-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(REPLACE(STR(?name), \"a\", \"_\") AS ?value) } ORDER BY ?value''', 3)
