from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("integer-boolean-cast", '''PREFIX ex: <https://example.org/chicago-consumer#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?value WHERE { ?s ex:rank ?rank . BIND(xsd:boolean(?rank) AS ?value) } ORDER BY ?value''', 3)

