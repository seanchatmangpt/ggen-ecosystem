from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("string-after", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(STRAFTER(CONCAT("head:", STR(?name)), ":") AS ?value) } ORDER BY ?value''', 3)

