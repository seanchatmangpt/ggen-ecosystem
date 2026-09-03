from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("sha256-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(SHA256(STR(?name)) AS ?value) } ORDER BY ?value''', 3)

