from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("substring-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(SUBSTR(STR(?name), 1, 2) AS ?value) } ORDER BY ?value''', 3)
