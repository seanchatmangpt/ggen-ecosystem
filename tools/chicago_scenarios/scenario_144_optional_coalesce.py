from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("optional-coalesce", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . OPTIONAL { ?s ex:missing ?missing } BIND(COALESCE(?missing, CONCAT("fallback:", STR(?name))) AS ?value) } ORDER BY ?value''', 3)

