from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("unbound-optional-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . OPTIONAL { ?s ex:missing ?missing } FILTER(!BOUND(?missing)) BIND(?name AS ?value) } ORDER BY ?value''', 3)

