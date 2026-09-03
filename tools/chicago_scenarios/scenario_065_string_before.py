from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("string-before", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(STRBEFORE(CONCAT(STR(?name), ":tail"), ":") AS ?value) } ORDER BY ?value''', 3)

