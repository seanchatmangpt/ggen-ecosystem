from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("sha1-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(SHA1(STR(?name)) AS ?value) } ORDER BY ?value''', 3)

