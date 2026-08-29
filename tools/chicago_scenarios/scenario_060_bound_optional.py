from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("bound-optional", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?rank . OPTIONAL { ?s ex:name ?name } FILTER(BOUND(?name)) BIND(?name AS ?value) } ORDER BY ?value''', 3)

