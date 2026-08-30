from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("concat-three-part", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(CONCAT("[", STR(?name), "]") AS ?value) } ORDER BY ?value''', 3)

