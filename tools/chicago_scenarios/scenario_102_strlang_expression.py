from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("strlang-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(STRLANG(STR(?name), "en") AS ?value) } ORDER BY ?value''', 3)

