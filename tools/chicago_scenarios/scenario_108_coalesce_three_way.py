from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("coalesce-three-way", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . OPTIONAL { ?s ex:firstMissing ?a } OPTIONAL { ?s ex:secondMissing ?b } BIND(COALESCE(?a, ?b, ?name) AS ?value) } ORDER BY ?value''', 3)

