from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("nested-subquery", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { { SELECT ?name WHERE { ?s ex:name ?name } ORDER BY ?name LIMIT 2 } BIND(?name AS ?value) } ORDER BY ?value''', 2)

